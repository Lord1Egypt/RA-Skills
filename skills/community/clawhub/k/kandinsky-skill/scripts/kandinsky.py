#!/usr/bin/env python3
"""
Kandinsky API — генерация и редактирование медиа (Kandinsky K6/K5, GigaAvatar).

Только стандартная библиотека Python, никаких зависимостей.

Адрес инстанса и ключ берутся из окружения:
  KANDINSKY_API_BASE  — адрес выданного вам инстанса (обязательно, дефолта нет)
  KANDINSKY_API_KEY   — ключ к этому инстансу (обязательно)

  python3 kandinsky.py t2i "закат в горах" -o out.png
  python3 kandinsky.py i2v cat.png "кот машет лапой" --quality hd -o cat.mp4
  python3 kandinsky.py health

ФАЙЛ СОБИРАЕТСЯ АВТОМАТИЧЕСКИ — не редактируй его руками.
Транспорт берётся из lib/kandinsky.py нативного расширения, операции и CLI —
из tools/clawhub_cli.py.in. Пересборка: python3 tools/build_clawhub.py
"""

import base64
import ipaddress
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Адреса по умолчанию нет намеренно: клиент не должен тянуть за собой чей-то
# инстанс, а навык — раскрывать его в публичном каталоге. Адрес задаёт вызывающий.
DEFAULT_BASE = ""

# Потолок на размер скачиваемого результата (OOM-защита от недоверенного/сбойного
# инстанса). Медиа Kandinsky на порядок меньше; 200 МБ — с большим запасом.
_MAX_RESULT_BYTES = 200 * 1024 * 1024
# Потолок для НЕ-результатных ответов (create/status/health): их тело — небольшой
# JSON, поэтому кап жёстче. Иначе сбойный/злой инстанс кладёт воркер гигантским
# телом статуса, которое ещё и поллится в цикле (та же OOM-защита, но на всех путях).
_MAX_STATUS_BYTES = 8 * 1024 * 1024
# Предел глубины обхода JSON результата: тело ответа приходит извне, и глубоко
# вложенная структура иначе упёрлась бы в предел рекурсии интерпретатора.
_MAX_JSON_DEPTH = 12


def _is_local_or_private(host):
    if host in ("localhost", "127.0.0.1", "::1"):
        return True
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        return False


class KandinskyError(RuntimeError):
    pass


class KandinskyTerminalError(KandinskyError):
    """Ошибка, которую повтором НЕ исправить: задача завершилась, но результат
    пустой/отклонён (нет медиа, цензура на этапе результата). В отличие от
    транзиентных ошибок (таймаут скачивания, 5xx, обрыв сети), повторный
    task_result вернёт то же самое — поэтому вызывающий не должен предлагать
    «забери позже»."""
    pass


# Классификация статусов задачи (сравниваем в нижнем регистре).
_STATUS_SUCCESS = {"done", "success", "completed", "succeeded", "ready", "finished", "ok"}
_STATUS_FAILURE = {"fail", "failed", "error", "errored", "cancelled", "canceled",
                   "rejected", "blocked", "denied", "moderation_failed", "censored", "aborted"}
_STATUS_QUEUED = {"new", "queued", "pending", "created", "accepted", "waiting"}
_STATUS_IN_PROGRESS = _STATUS_QUEUED | {"processing", "running", "started", "in_progress", "generating"}
# Сколько секунд ждать в очереди без смены статуса, прежде чем счесть задачу застрявшей.
_STUCK_QUEUE_SEC = 90
# Признаки того, что задачу отклонила цензура/модерация.
_CENSOR_HINTS = ("censor", "цензур", "moderation", "модерац", "block", "заблок", "запрещ",
                 "отклон", "policy", "nsfw", "18+", "safety")

# Предупреждение о незащищённом транспорте печатается один раз за время жизни
# процесса: клиент создаётся на каждый вызов инструмента, и без этого флага журнал
# засорялся бы одинаковой строкой. Пользователю оно всё равно видно в kandinsky_health.
_insecure_warned = False


def _extract_reason(info):
    """Достаёт человекочитаемую причину из тела статуса задачи."""
    if not isinstance(info, dict):
        return ""
    for k in ("error", "message", "detail", "reason", "description",
              "error_message", "comment", "status_message"):
        v = info.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
        if isinstance(v, dict):
            for kk in ("message", "detail", "reason"):
                vv = v.get(kk)
                if isinstance(vv, str) and vv.strip():
                    return vv.strip()
    return ""


def _looks_censored(status_norm, reason):
    blob = f"{status_norm or ''} {reason or ''}".lower()
    return any(h in blob for h in _CENSOR_HINTS)


def _friendly_http_error(code, where, body):
    """Человекочитаемая ошибка вместо сырого дампа HTTP-тела для типовых кодов
    (лимиты, авторизация, серверные сбои)."""
    detail = ""
    try:
        obj = json.loads(body)
        d = obj.get("detail") if isinstance(obj, dict) else None
        if isinstance(d, dict):
            detail = d.get("message") or d.get("code") or ""
        elif isinstance(d, str):
            detail = d
        elif isinstance(obj, dict):
            detail = obj.get("message") or obj.get("error") or ""
    except Exception:
        pass
    detail = (detail or "").strip()
    tail = f": {detail}" if detail else ""
    if code == 429:
        return ("Достигнут лимит запросов к Kandinsky API (rate limit / квота исчерпана). "
                "Подожди немного и попробуй снова" + (tail or "."))
    if code in (401, 403):
        return ("Ошибка авторизации Kandinsky API — проверь KANDINSKY_API_KEY в настройках "
                "навыка" + (tail or "."))
    if code == 404:
        return f"Kandinsky API: ресурс не найден (HTTP 404 на {where}){tail}"
    if 500 <= code < 600:
        return (f"Сервер Kandinsky временно недоступен (HTTP {code}). Попробуй позже" + (tail or "."))
    return f"HTTP {code} на {where}{tail or (': ' + body[:300])}"


class KandinskyClient:
    def __init__(self, api_key=None, base=None, timeout=120, allow_insecure=False):
        self.api_key = api_key or os.environ.get("KANDINSKY_API_KEY")
        self.base = (base or os.environ.get("KANDINSKY_API_BASE") or DEFAULT_BASE).rstrip("/")
        self.timeout = timeout
        if not self.api_key:
            raise KandinskyError(
                "Нет ключа. Задай переменную окружения KANDINSKY_API_KEY "
                "или передай api_key= в KandinskyClient(). Если доступа к Kandinsky API "
                "ещё нет, запросить его можно на kandinsky@kandinskylab.ai."
            )
        if not self.base:
            raise KandinskyError(
                "Не задан адрес API. Задай переменную окружения KANDINSKY_API_BASE "
                "или передай base= в KandinskyClient(). Если доступа к Kandinsky API "
                "ещё нет, запросить его можно на kandinsky@kandinskylab.ai."
            )
        self._check_transport(allow_insecure)

    def _check_transport(self, allow_insecure):
        """Не даём слать API-ключ по plain HTTP в недоверенную сеть."""
        parts = urllib.parse.urlparse(self.base)
        if parts.scheme == "https":
            return
        if parts.scheme == "http" and _is_local_or_private(parts.hostname or ""):
            return  # loopback/приватный доверенный инстанс — ок
        msg = (
            f"Небезопасный транспорт: {self.base} использует plain HTTP в публичной "
            "сети — API-ключ может быть перехвачен. Используй HTTPS либо "
            "loopback/приватный доверенный адрес. Чтобы продолжить осознанно, передай "
            "allow_insecure=True или KANDINSKY_ALLOW_INSECURE=1."
        )
        if allow_insecure or os.environ.get("KANDINSKY_ALLOW_INSECURE") == "1":
            global _insecure_warned
            if not _insecure_warned:
                _insecure_warned = True
                print(f"[warn] {msg}", file=sys.stderr)
            return
        raise KandinskyError(msg)

    def health(self):
        """Дешёвый префлайт: жив ли сервис. Возвращает тело /health."""
        ctype, raw = self._request("GET", "/health")
        if "application/json" in ctype:
            return json.loads(raw.decode("utf-8"))
        return raw.decode("utf-8", "replace")

    # ---- низкоуровневые HTTP-хелперы -------------------------------------

    def _request(self, method, path, json_body=None, timeout=None, max_bytes=None):
        url = self.base + path
        data = None
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                ctype = resp.headers.get("Content-Type", "")
                # Читаем с лимитом ВСЕГДА: недоверенный/сбойный инстанс не должен
                # положить воркер гигантским телом ответа (OOM-защита). Для результата
                # кап большой (передаётся явно), для статуса/create/health — жёсткий дефолт.
                cap = max_bytes if max_bytes is not None else _MAX_STATUS_BYTES
                raw = b""
                while True:
                    chunk = resp.read(1 << 16)
                    if not chunk:
                        break
                    raw += chunk
                    if len(raw) > cap:
                        raise KandinskyError(
                            f"Ответ Kandinsky превышает лимит {cap} байт — приём прерван "
                            "для защиты памяти.")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            raise KandinskyError(_friendly_http_error(e.code, f"{method} {path}", body)) from None
        except urllib.error.URLError as e:
            raise KandinskyError(f"Не удалось подключиться к {url}: {e.reason}") from None
        return ctype, raw

    def create_task(self, path, params, censor=True):
        """Создать задачу генерации. Возвращает task_id (без ожидания)."""
        ctype, raw = self._request("POST", path, {"censor": censor, "params": params})
        try:
            obj = json.loads(raw.decode("utf-8"))
        except Exception:
            raise KandinskyError(
                "Неожиданный ответ при создании задачи (не JSON): "
                + raw.decode("utf-8", "replace")[:200]) from None
        if not isinstance(obj, dict):
            raise KandinskyError(f"Неожиданный ответ при создании задачи: {str(obj)[:200]}")
        task_id = obj.get("task_id")
        if not task_id:
            raise KandinskyError(f"В ответе нет task_id: {obj}")
        return task_id

    # ---- статус / результат / ожидание ----------------------------------

    def _task_info(self, task_id):
        """Полное тело статуса задачи (dict) — чтобы достать не только status,
        но и причину ошибки/сообщение цензора."""
        _, raw = self._request("GET", f"/tasks/{task_id}")
        try:
            obj = json.loads(raw.decode("utf-8"))
            return obj if isinstance(obj, dict) else {"status": obj}
        except Exception:
            return {}

    def status(self, task_id):
        return self._task_info(task_id).get("status")

    def wait(self, task_id, poll=None, timeout=240, on_update=None):
        """Поллит статус до терминального. Возвращает финальный статус (успех).

        Дефолт 240 с выбран не по длительности генерации, а по бюджету хоста:
        и расширение, и скриптовая версия живут внутри лимита 300 с на один
        вызов. Ждать дольше бессмысленно — процесс всё равно убьют, и вместо
        понятного «таймаут, вот task_id» получится обрыв. Вызывающий может
        передать свой бюджет явно.

        Важно: не залипаем на нестандартных/пустых/застрявших статусах — быстро
        отдаём понятную ошибку вместо молчаливого ожидания до таймаута.

        poll=None → адаптивный интервал (быстрый первый опрос для лёгких картинок,
        плавный рост до потолка для длинных видео). poll=<число> → фиксированный."""
        start = time.time()
        last = None
        last_change = start
        interval = 2.0 if poll is None else float(poll)
        while True:
            info = self._task_info(task_id)
            st = info.get("status")
            norm = st.strip().lower() if isinstance(st, str) else st
            if st != last:
                last = st
                last_change = time.time()
                if on_update:
                    on_update(st)

            if norm in _STATUS_SUCCESS:
                return st
            if norm in _STATUS_FAILURE:
                reason = _extract_reason(info)
                if _looks_censored(norm, reason):
                    raise KandinskyError(
                        "Запрос отклонён цензурой" + (f": {reason}" if reason else "")
                        + ". Переформулируй промпт или замени входные изображения.")
                raise KandinskyError(
                    f"Задача завершилась с ошибкой (статус '{st}')" + (f": {reason}" if reason else ""))
            if not norm:
                raise KandinskyError(
                    f"Пустой/непонятный ответ статуса задачи {task_id}: "
                    f"{json.dumps(info, ensure_ascii=False)[:200]}")
            if norm not in _STATUS_IN_PROGRESS:
                # неизвестный не-прогресс статус — считаем терминальным, не ждём впустую
                reason = _extract_reason(info)
                raise KandinskyError(
                    f"Неизвестный статус задачи '{st}'" + (f": {reason}" if reason else "")
                    + " — останавливаюсь, чтобы не ждать зря.")
            # застревание в очереди (типичный случай superres: воркер не берёт задачу)
            if norm in _STATUS_QUEUED and (time.time() - last_change) > _STUCK_QUEUE_SEC:
                raise KandinskyError(
                    f"Задача застряла в очереди (статус '{st}' > {_STUCK_QUEUE_SEC} с): "
                    "воркер не взял задачу. Попробуй позже или другое разрешение.")
            if time.time() - start > timeout:
                raise KandinskyError(f"Таймаут ожидания задачи {task_id} (последний статус '{st}').")
            time.sleep(interval)
            if poll is None:
                interval = min(interval * 1.5, 10.0)

    def result(self, task_id, out=None, download_timeout=None):
        """Забирает результат. Сохраняет в файл out (если задан) и возвращает путь/данные.

        download_timeout — сокет-таймаут на скачивание. По умолчанию с запасом на
        большое видео; вызывающий может ужать его под оставшийся бюджет, чтобы не
        перескочить манифестный timeout_sec."""
        dl = download_timeout if download_timeout is not None else max(self.timeout, 300)
        ctype, raw = self._request("GET", f"/tasks/{task_id}/result",
                                   timeout=dl, max_bytes=_MAX_RESULT_BYTES)
        payload = raw
        if "application/json" in ctype:
            obj = json.loads(raw.decode("utf-8"))
            media = _extract_media_bytes(obj)
            if media is not None:
                payload = media
            else:
                # JSON без извлекаемого медиа — это НЕ картинка/видео, а ошибка,
                # статус или ссылка. Нельзя записать этот текст в файл с медиа-
                # расширением: агент показал бы «битую картинку» и выдал бы сбой
                # за успех. Это ТЕРМИНАЛЬНО (повтор не поможет) → KandinskyTerminalError.
                reason = _extract_reason(obj) if isinstance(obj, dict) else ""
                if _looks_censored("", reason):
                    # цензура иногда всплывает только на этапе результата, хотя
                    # статус задачи был «успех» — сохраняем дружелюбную формулировку.
                    raise KandinskyTerminalError(
                        "Запрос отклонён цензурой" + (f": {reason}" if reason else "")
                        + ". Переформулируй промпт или замени входные изображения.")
                raise KandinskyTerminalError(
                    "В ответе результата нет медиа-данных"
                    + (f": {reason}" if reason
                       else f" (получен JSON без картинки/видео: "
                            f"{json.dumps(obj, ensure_ascii=False)[:200]})"))
        if out:
            with open(out, "wb") as f:
                f.write(payload)
            return out
        return payload


# ---- утилиты -------------------------------------------------------------

def _decode_b64(s):
    """Декодирует правдоподобную base64-строку в bytes или None.

    В отличие от старой эвристики «длина > 64», реально валидирует base64 и
    проверяет, что результат похож на медиа (не короткая строка вроде id/URL/лога).
    Поддерживает data-URI (`data:image/png;base64,...`)."""
    if not isinstance(s, str) or len(s) < 64:
        return None
    core = s.split(",", 1)[1] if s.startswith("data:") and "," in s else s
    core = "".join(core.split())  # убрать переводы строк/пробелы
    try:
        raw = base64.b64decode(core, validate=True)
    except Exception:
        return None
    return raw if len(raw) >= 100 else None


def _extract_media_bytes(obj, _depth=0):
    """Рекурсивно ищет в JSON-ответе первую валидную base64-строку с медиа и
    возвращает декодированные bytes (или None). Сначала смотрит осмысленные ключи.

    Глубина ограничена _MAX_JSON_DEPTH: ответ инстанса — чужие данные, и на
    глубоко вложенной структуре рекурсия упёрлась бы в предел интерпретатора.
    Медиа лежит у самой поверхности ответа, так что потерять его лимит не может."""
    if _depth > _MAX_JSON_DEPTH:
        return None
    keys = ("image", "video", "file", "result", "data", "content", "b64", "base64", "audio")
    if isinstance(obj, dict):
        for k in keys:
            v = obj.get(k)
            if isinstance(v, str):
                d = _decode_b64(v)
                if d is not None:
                    return d
            elif isinstance(v, list):
                for it in v:
                    if isinstance(it, str):
                        d = _decode_b64(it)
                        if d is not None:
                            return d
        for v in obj.values():
            d = _extract_media_bytes(v, _depth + 1)
            if d is not None:
                return d
    elif isinstance(obj, list):
        for v in obj:
            # список строк (напр. {"images": ["<base64>"]}) — пробуем декодировать
            # напрямую: иначе media под нестандартным ключом-массивом теряется.
            d = _decode_b64(v) if isinstance(v, str) else _extract_media_bytes(v, _depth + 1)
            if d is not None:
                return d
    return None

# =========================================================================
# Ниже — часть, которой нет в нативном расширении: операции Kandinsky поверх
# транспорта и интерфейс командной строки. В расширении эту роль играют
# core/endpoints.py и plugin.py; здесь запускающая сторона — не агент, а
# человек или скрипт, поэтому всё сведено в один исполняемый файл.
# =========================================================================

import argparse

# Бюджет одного запуска. Хост, который запускает этот скрипт как навык, убивает
# процесс на 300 с — ждать дольше нельзя: вместо понятного «таймаут, вот task_id»
# получился бы обрыв на полуслове. Человек из оболочки может поднять --timeout.
_WAIT_BUDGET_SEC = 240
_MIN_DOWNLOAD_SEC = 30
_MAX_BUDGET_SEC = 3600

# Ограничения маршрутов — те же, что в нативной версии (core/endpoints.py).
RES_T2I = ("1024x1024", "768x768", "768x1280", "1280x768", "auto")
RES_T2V_LITE = ("512x512", "512x768", "768x512")
RES_T2V_PRO = ("768x1280", "1280x768")
BEAUTIFICATOR = ("enabled", "disabled", "gigachat-max")
QUALITY_PATHS = {"lite": "/tasks/k5-i2v-lite", "sd": "/tasks/k5-i2v-sd", "hd": "/tasks/k5-i2v-hd"}


def out_roots():
    """Каталоги, куда разрешено писать результат — по убыванию приоритета.

    Скрипт живёт в двух мирах. У человека в оболочке рабочий каталог и есть
    ответ: пишем рядом, как любая утилита. Под управлением агента рабочим
    каталогом оказывается каталог самого навыка — писать туда нельзя: хост
    считает такой файл подменой payload и блокирует следующий запуск. Поэтому
    там разрешены только каталог состояния навыка и каталог, который явно
    назначил владелец инстанса (KANDINSKY_OUT_DIR).
    """
    roots = []
    custom = os.environ.get("KANDINSKY_OUT_DIR", "").strip()
    if custom:
        roots.append(custom)
    state = os.environ.get("OUROBOROS_SKILL_STATE_DIR", "").strip()
    if state:
        roots.append(os.path.join(state, "out"))
    return roots or [os.getcwd()]


def resolve_out(path, default_name):
    """Путь результата, ограниченный разрешёнными каталогами.

    Относительный путь считается от первого разрешённого каталога, а не от
    рабочего: под агентом рабочий каталог — каталог навыка, и `-o out.png`
    молча ломал бы навык. Абсолютный путь проверяется по реальному пути
    (realpath), поэтому ни `..`, ни симлинк наружу не проходят.
    """
    roots = out_roots()
    target = os.path.join(roots[0], default_name) if not path else (
        path if os.path.isabs(path) else os.path.join(roots[0], path))
    parent = os.path.realpath(os.path.dirname(target) or ".")
    for root in roots:
        real_root = os.path.realpath(root)
        if parent == real_root or parent.startswith(real_root + os.sep):
            os.makedirs(parent, exist_ok=True)
            return os.path.join(parent, os.path.basename(target))
    raise KandinskyError(
        f"Путь '{path}' вне разрешённых каталогов ({', '.join(roots)}). "
        "Укажи файл внутри одного из них.")


def to_b64(src):
    """Путь к файлу, bytes или уже готовая base64-строка → base64.

    Чтение произвольного файла здесь намеренно: команду запускает человек и сам
    указывает файл. В нативном расширении такой функции нет — там источник
    приходит от модели, поэтому чтение ограничено рабочим каталогом агента.
    """
    if isinstance(src, bytes):
        return base64.b64encode(src).decode("ascii")
    if isinstance(src, str) and os.path.exists(src):
        with open(src, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    return src  # считаем, что уже base64


class Kandinsky(KandinskyClient):
    """Транспорт KandinskyClient + операции генерации.

    Как библиотека:
        from kandinsky import Kandinsky
        k = Kandinsky()                       # ключ и адрес — из окружения
        k.generate_image("кот в скафандре", out="cat.png")
        k.animate_image("cat.png", "кот машет лапой", out="cat.mp4")
    """

    def run(self, path, params, censor=True, out=None, poll=None, timeout=None, verbose=True):
        """Создать задачу → дождаться → забрать результат.

        Ожидание и скачивание укладываются в один бюджет: иначе скачивание
        большого видео начиналось бы уже за пределами лимита хоста."""
        budget = _WAIT_BUDGET_SEC if timeout is None else float(timeout)
        start = time.time()
        task_id = self.create_task(path, params, censor=censor)
        if verbose:
            print(f"[task] {task_id} создан", file=sys.stderr)
        self.wait(task_id, poll=poll, timeout=max(1.0, budget - (time.time() - start)),
                  on_update=(lambda s: print(f"[task] {task_id}: {s}", file=sys.stderr)) if verbose else None)
        left = budget - (time.time() - start)
        return self.result(task_id, out=out, download_timeout=max(_MIN_DOWNLOAD_SEC, left))

    def _beaut(self, params, beautificator):
        if beautificator:
            if beautificator not in BEAUTIFICATOR:
                raise KandinskyError(f"beautificator: {' | '.join(BEAUTIFICATOR)}")
            params["beautificator"] = beautificator
        return params

    def generate_image(self, query, resolution="1024x1024", beautificator=None,
                       censor=True, out=None, **kw):
        if not query:
            raise KandinskyError("Не задан query — текст запроса обязателен")
        resolution = resolution or "1024x1024"
        if resolution not in RES_T2I:
            raise KandinskyError(f"Недопустимое разрешение '{resolution}'. Допустимо: {', '.join(RES_T2I)}.")
        params = self._beaut({"query": query, "resolution": resolution}, beautificator)
        return self.run("/tasks/k6-image-t2i", params, censor=censor, out=out, **kw)

    def edit_image(self, images, query, beautificator=None, censor=True, out=None, **kw):
        if not query:
            raise KandinskyError("Не задан query — опиши, что изменить")
        srcs = images if isinstance(images, (list, tuple)) else [images]
        srcs = [s for s in srcs if s]
        if not srcs:
            raise KandinskyError("Не задан источник: нужна хотя бы одна картинка")
        params = self._beaut({"query": query, "image": [to_b64(s) for s in srcs]}, beautificator)
        return self.run("/tasks/k6-i2i", params, censor=censor, out=out, **kw)

    def upscale(self, image, upscale=2, one_step_t=None, censor=True, out=None, **kw):
        if not image:
            raise KandinskyError("Не задана картинка")
        try:
            up = 2 if upscale is None else int(upscale)
        except (TypeError, ValueError):
            raise KandinskyError("upscale должен быть числом 2 или 4") from None
        if up not in (2, 4):
            raise KandinskyError("upscale может быть только 2 или 4")
        params = {"image": to_b64(image), "upscale": up}
        if one_step_t is not None:
            try:
                ost = float(one_step_t)
            except (TypeError, ValueError):
                raise KandinskyError("one_step_t должен быть числом от 0 до 1") from None
            if not 0.0 <= ost <= 1.0:
                raise KandinskyError("one_step_t вне диапазона: допустимо 0..1")
            params["one_step_t"] = ost
        return self.run("/tasks/k6_superres", params, censor=censor, out=out, **kw)

    def text_to_video(self, query, resolution=None, pro=False, beautificator=None,
                      censor=True, out=None, **kw):
        if not query:
            raise KandinskyError("Не задан query — текст запроса обязателен")
        allowed = RES_T2V_PRO if pro else RES_T2V_LITE
        resolution = resolution or ("1280x768" if pro else "768x512")
        if resolution not in allowed:
            raise KandinskyError(
                f"Недопустимое разрешение '{resolution}' для режима "
                f"{'pro' if pro else 'lite'}. Допустимо: {', '.join(allowed)}.")
        path = "/tasks/k5_video_t2v_pro" if pro else "/tasks/k5_video_t2v_lite"
        params = self._beaut({"query": query, "resolution": resolution}, beautificator)
        return self.run(path, params, censor=censor, out=out, **kw)

    def animate_image(self, image, query, quality="lite", beautificator=None,
                      censor=True, out=None, **kw):
        if not image or not query:
            raise KandinskyError("Нужны и картинка, и query — промпт движения")
        path = QUALITY_PATHS.get(quality or "lite")
        if not path:
            raise KandinskyError(f"quality: {' | '.join(QUALITY_PATHS)}")
        params = self._beaut({"query": query, "image": to_b64(image)}, beautificator)
        return self.run(path, params, censor=censor, out=out, **kw)

    def avatar(self, image, audio, query="", censor=True, out=None, **kw):
        if not image or not audio:
            raise KandinskyError("Нужны и фотография, и аудиофайл")
        params = {"query": query or "", "image": to_b64(image), "audio": to_b64(audio)}
        return self.run("/tasks/giga_avatar", params, censor=censor, out=out, **kw)


# ---- CLI -----------------------------------------------------------------

def _build_parser():
    p = argparse.ArgumentParser(
        prog="kandinsky",
        description="Генерация и редактирование медиа через Kandinsky API. "
                    "Адрес инстанса и ключ берутся из KANDINSKY_API_BASE и KANDINSKY_API_KEY.")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("t2i", help="текст → картинка")
    a.add_argument("query")
    a.add_argument("--resolution", default="1024x1024", choices=list(RES_T2I))
    a.add_argument("--beautificator", choices=list(BEAUTIFICATOR))
    a.add_argument("-o", "--out", default=None,
                   help="файл результата (по умолчанию — в разрешённом каталоге)")

    a = sub.add_parser("i2i", help="картинка(и) + текст → картинка")
    a.add_argument("image", nargs="+")
    a.add_argument("query")
    a.add_argument("--beautificator", choices=list(BEAUTIFICATOR))
    a.add_argument("-o", "--out", default=None,
                   help="файл результата (по умолчанию — в разрешённом каталоге)")

    a = sub.add_parser("superres", help="апскейл ×2/×4")
    a.add_argument("image")
    a.add_argument("--upscale", type=int, default=2, choices=[2, 4])
    a.add_argument("--one-step-t", type=float, default=None,
                   help="0..1 — сила следования оригиналу")
    a.add_argument("-o", "--out", default=None)

    a = sub.add_parser("t2v", help="текст → видео")
    a.add_argument("query")
    a.add_argument("--resolution", default=None,
                   help=f"lite: {'|'.join(RES_T2V_LITE)}; pro: {'|'.join(RES_T2V_PRO)}")
    a.add_argument("--pro", action="store_true", help="качественнее и дольше")
    a.add_argument("--beautificator", choices=list(BEAUTIFICATOR))
    a.add_argument("-o", "--out", default=None)

    a = sub.add_parser("i2v", help="картинка → видео (оживить)")
    a.add_argument("image")
    a.add_argument("query", help="промпт движения объекта, не только камеры")
    a.add_argument("--quality", default="lite", choices=list(QUALITY_PATHS))
    a.add_argument("--beautificator", choices=list(BEAUTIFICATOR))
    a.add_argument("-o", "--out", default=None)

    a = sub.add_parser("avatar", help="фото + аудио → говорящий аватар")
    a.add_argument("image")
    a.add_argument("audio")
    a.add_argument("query", nargs="?", default="")
    a.add_argument("-o", "--out", default=None)

    sub.add_parser("health", help="префлайт: жив ли сервис")

    a = sub.add_parser("status", help="статус задачи")
    a.add_argument("task_id")

    a = sub.add_parser("result", help="забрать результат задачи")
    a.add_argument("task_id")
    a.add_argument("-o", "--out", default=None)

    for name in ("t2i", "i2i", "superres", "t2v", "i2v", "avatar"):
        sub.choices[name].add_argument("--no-censor", action="store_true",
                                       help="отключить фильтр контента")
    for name in sub.choices:
        sub.choices[name].add_argument("--base", default=None,
                                       help="адрес инстанса (иначе KANDINSKY_API_BASE)")
        sub.choices[name].add_argument("--allow-insecure", action="store_true",
                                       help="разрешить plain HTTP в публичной сети (небезопасно)")
        sub.choices[name].add_argument("--quiet", action="store_true",
                                       help="не печатать ход выполнения")
        sub.choices[name].add_argument("--timeout", type=float, default=None,
                                       help=f"бюджет ожидания в секундах "
                                            f"(по умолчанию {_WAIT_BUDGET_SEC}; "
                                            f"под управлением агента поднимать бесполезно — "
                                            f"хост обрывает вызов на 300 с)")
    return p


def _budget(args):
    """Бюджет ожидания из --timeout, с проверкой границ."""
    if getattr(args, "timeout", None) is None:
        return None
    budget = float(args.timeout)
    if not 1.0 <= budget <= _MAX_BUDGET_SEC:
        raise KandinskyError(f"--timeout вне диапазона: допустимо 1..{_MAX_BUDGET_SEC} с")
    return budget


def main(argv=None):
    args = _build_parser().parse_args(argv)
    k = Kandinsky(base=args.base, allow_insecure=args.allow_insecure)
    censor = not getattr(args, "no_censor", False)
    common = {"censor": censor, "verbose": not args.quiet, "timeout": _budget(args)}
    cmd = args.cmd

    if cmd == "health":
        h = k.health()
        print(json.dumps(h, ensure_ascii=False) if isinstance(h, dict) else h)
        return
    if cmd == "status":
        print(k.status(args.task_id))
        return

    if cmd == "t2i":
        out = k.generate_image(args.query, resolution=args.resolution,
                               beautificator=args.beautificator,
                               out=resolve_out(args.out, "kandinsky.png"), **common)
    elif cmd == "i2i":
        out = k.edit_image(args.image, args.query, beautificator=args.beautificator,
                           out=resolve_out(args.out, "kandinsky-edit.png"), **common)
    elif cmd == "superres":
        out = k.upscale(args.image, upscale=args.upscale, one_step_t=args.one_step_t,
                        out=resolve_out(args.out, "kandinsky-upscaled.png"), **common)
    elif cmd == "t2v":
        out = k.text_to_video(args.query, resolution=args.resolution, pro=args.pro,
                              beautificator=args.beautificator,
                              out=resolve_out(args.out, "kandinsky.mp4"), **common)
    elif cmd == "i2v":
        out = k.animate_image(args.image, args.query, quality=args.quality,
                              beautificator=args.beautificator,
                              out=resolve_out(args.out, "kandinsky-animated.mp4"), **common)
    elif cmd == "avatar":
        out = k.avatar(args.image, args.audio, args.query,
                       out=resolve_out(args.out, "kandinsky-avatar.mp4"), **common)
    elif cmd == "result":
        # Дозабор тоже живёт внутри бюджета хоста: сокет-таймаут по умолчанию
        # (300 с) ровно равен лимиту, за который процесс уже убивают.
        out = k.result(args.task_id, out=resolve_out(args.out, "kandinsky-result.bin"),
                       download_timeout=_budget(args) or _WAIT_BUDGET_SEC)
    else:
        raise KandinskyError(f"Неизвестная команда: {cmd}")

    print(f"Готово: {out}")


if __name__ == "__main__":
    try:
        main()
    except KandinskyError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
