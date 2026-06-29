#!/usr/bin/env python3
"""
Kandinsky API client (Kandinsky K6/K5 + GigaAvatar).

Только стандартная библиотека Python — никаких зависимостей.

Авторизация и адрес берутся из окружения:
  KANDINSKY_API_KEY  — API-ключ (обязательно)
  KANDINSKY_API_BASE   — база API (опц., по умолчанию http://87.242.117.37:5051)

Использование как библиотеки:
  from kandinsky import KandinskyClient
  c = KandinskyClient()
  path = c.generate_image("кот в скафандре", resolution="1024x1024", out="cat.png")
  vid  = c.animate_image("cat.png", "кот машет лапой", quality="lite", out="cat.mp4")

Использование как CLI:
  python kandinsky.py t2i  "закатные горы" --resolution 1024x1024 -o out.png
  python kandinsky.py i2i  in.png "в стиле акварели" -o out.png
  python kandinsky.py superres in.png --upscale 2 -o big.png
  python kandinsky.py t2v  "волны на берегу" --pro -o clip.mp4
  python kandinsky.py i2v  in.png "камера медленно облетает" --quality hd -o clip.mp4
  python kandinsky.py avatar face.png speech.wav "говорящий аватар" -o avatar.mp4
  python kandinsky.py status <task_id>
  python kandinsky.py result <task_id> -o out.bin
"""

import argparse
import base64
import ipaddress
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = "http://87.242.117.37:5051"


def _is_local_or_private(host):
    if host in ("localhost", "127.0.0.1", "::1"):
        return True
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        return False


class KandinskyError(RuntimeError):
    pass


class KandinskyClient:
    def __init__(self, api_key=None, base=None, timeout=120, allow_insecure=False):
        self.api_key = api_key or os.environ.get("KANDINSKY_API_KEY")
        self.base = (base or os.environ.get("KANDINSKY_API_BASE") or DEFAULT_BASE).rstrip("/")
        self.timeout = timeout
        if not self.api_key:
            raise KandinskyError(
                "Нет ключа. Задай переменную окружения KANDINSKY_API_KEY "
                "или передай api_key= в KandinskyClient()."
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

    def _request(self, method, path, json_body=None):
        url = self.base + path
        data = None
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                ctype = resp.headers.get("Content-Type", "")
                raw = resp.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            raise KandinskyError(f"HTTP {e.code} on {method} {path}: {body}") from None
        except urllib.error.URLError as e:
            raise KandinskyError(f"Не удалось подключиться к {url}: {e.reason}") from None
        return ctype, raw

    def _post_task(self, path, params, censor=True):
        ctype, raw = self._request("POST", path, {"censor": censor, "params": params})
        obj = json.loads(raw.decode("utf-8"))
        task_id = obj.get("task_id")
        if not task_id:
            raise KandinskyError(f"В ответе нет task_id: {obj}")
        return task_id

    # ---- статус / результат / ожидание ----------------------------------

    def status(self, task_id):
        _, raw = self._request("GET", f"/tasks/{task_id}")
        return json.loads(raw.decode("utf-8")).get("status")

    def wait(self, task_id, poll=6, timeout=900, on_update=None):
        """Поллит статус до done/fail. Возвращает финальный статус."""
        start = time.time()
        last = None
        while True:
            st = self.status(task_id)
            if st != last and on_update:
                on_update(st)
            last = st
            if st in ("done", "success", "completed"):
                return st
            if st in ("fail", "failed", "error"):
                raise KandinskyError(f"Задача {task_id} завершилась со статусом '{st}'")
            if time.time() - start > timeout:
                raise KandinskyError(f"Таймаут ожидания задачи {task_id} (последний статус '{st}')")
            time.sleep(poll)

    def result(self, task_id, out=None):
        """Забирает результат. Сохраняет в файл out (если задан) и возвращает путь/данные."""
        ctype, raw = self._request("GET", f"/tasks/{task_id}/result")
        # результат может прийти как JSON с base64 или как бинарь
        payload = raw
        if "application/json" in ctype:
            obj = json.loads(raw.decode("utf-8"))
            b64 = _find_base64(obj)
            if b64 is not None:
                payload = base64.b64decode(b64)
            else:
                if out:
                    with open(out, "w", encoding="utf-8") as f:
                        json.dump(obj, f, ensure_ascii=False, indent=2)
                    return out
                return obj
        if out:
            with open(out, "wb") as f:
                f.write(payload)
            return out
        return payload

    def run(self, path, params, censor=True, out=None, poll=6, timeout=900, verbose=True):
        """Создать задачу → дождаться → забрать результат. Возвращает путь/данные."""
        task_id = self._post_task(path, params, censor=censor)
        if verbose:
            print(f"[task] {task_id} создан", file=sys.stderr)
        self.wait(task_id, poll=poll, timeout=timeout,
                  on_update=(lambda s: print(f"[task] {task_id}: {s}", file=sys.stderr)) if verbose else None)
        return self.result(task_id, out=out)

    # ---- высокоуровневые методы по эндпоинтам ----------------------------

    def generate_image(self, query, resolution="1024x1024", beautificator=None,
                       censor=True, out=None):
        params = {"query": query, "resolution": resolution}
        if beautificator:
            params["beautificator"] = beautificator
        return self.run("/tasks/k6-image-t2i", params, censor=censor, out=out)

    def edit_image(self, images, query, beautificator=None, censor=True, out=None):
        imgs = [_to_b64(i) for i in (images if isinstance(images, (list, tuple)) else [images])]
        params = {"query": query, "image": imgs}
        if beautificator:
            params["beautificator"] = beautificator
        return self.run("/tasks/k6-i2i", params, censor=censor, out=out)

    def upscale(self, image, upscale=2, one_step_t=None, censor=True, out=None):
        if upscale not in (2, 4):
            raise KandinskyError("upscale может быть только 2 или 4")
        params = {"image": _to_b64(image), "upscale": upscale}
        if one_step_t is not None:
            params["one_step_t"] = one_step_t
        return self.run("/tasks/k6_superres", params, censor=censor, out=out)

    def text_to_video(self, query, resolution=None, pro=False, beautificator=None,
                      censor=True, out=None):
        path = "/tasks/k5_video_t2v_pro" if pro else "/tasks/k5_video_t2v_lite"
        if resolution is None:
            resolution = "1280x768" if pro else "768x512"
        params = {"query": query, "resolution": resolution}
        if beautificator:
            params["beautificator"] = beautificator
        return self.run(path, params, censor=censor, out=out)

    def animate_image(self, image, query, quality="lite", beautificator=None,
                      censor=True, out=None):
        path = {
            "lite": "/tasks/k5-i2v-lite",
            "sd": "/tasks/k5-i2v-sd",
            "hd": "/tasks/k5-i2v-hd",
        }.get(quality)
        if not path:
            raise KandinskyError("quality: lite | sd | hd")
        params = {"query": query, "image": _to_b64(image)}
        if beautificator:
            params["beautificator"] = beautificator
        return self.run(path, params, censor=censor, out=out)

    def avatar(self, image, audio, query, censor=True, out=None):
        params = {"query": query, "image": _to_b64(image), "audio": _to_b64(audio)}
        return self.run("/tasks/giga_avatar", params, censor=censor, out=out)


# ---- утилиты -------------------------------------------------------------

def _to_b64(src):
    """src: путь к файлу, bytes, или уже base64-строка."""
    if isinstance(src, bytes):
        return base64.b64encode(src).decode("ascii")
    if isinstance(src, str) and os.path.exists(src):
        with open(src, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    # считаем, что уже base64
    return src


def _find_base64(obj):
    """Рекурсивно ищет первую правдоподобную base64-строку в JSON-ответе."""
    keys = ("image", "video", "file", "result", "data", "content", "b64", "base64")
    if isinstance(obj, dict):
        for k in keys:
            v = obj.get(k)
            if isinstance(v, str) and len(v) > 64:
                return v
            if isinstance(v, list) and v and isinstance(v[0], str) and len(v[0]) > 64:
                return v[0]
        for v in obj.values():
            found = _find_base64(v)
            if found:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = _find_base64(v)
            if found:
                return found
    return None


# ---- CLI -----------------------------------------------------------------

def _build_parser():
    p = argparse.ArgumentParser(description="Kandinsky API client")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("t2i", help="текст → картинка")
    a.add_argument("query"); a.add_argument("--resolution", default="1024x1024")
    a.add_argument("--beautificator"); a.add_argument("-o", "--out", default="out.png")

    a = sub.add_parser("i2i", help="картинка(и)+текст → картинка")
    a.add_argument("image", nargs="+"); a.add_argument("query")
    a.add_argument("--beautificator"); a.add_argument("-o", "--out", default="out.png")

    a = sub.add_parser("superres", help="апскейл ×2/×4")
    a.add_argument("image"); a.add_argument("--upscale", type=int, default=2, choices=[2, 4])
    a.add_argument("--one-step-t", type=float, default=None)
    a.add_argument("-o", "--out", default="upscaled.png")

    a = sub.add_parser("t2v", help="текст → видео")
    a.add_argument("query"); a.add_argument("--resolution", default=None)
    a.add_argument("--pro", action="store_true"); a.add_argument("--beautificator")
    a.add_argument("-o", "--out", default="video.mp4")

    a = sub.add_parser("i2v", help="картинка → видео")
    a.add_argument("image"); a.add_argument("query")
    a.add_argument("--quality", default="lite", choices=["lite", "sd", "hd"])
    a.add_argument("--beautificator"); a.add_argument("-o", "--out", default="video.mp4")

    a = sub.add_parser("avatar", help="фото+аудио → говорящий аватар")
    a.add_argument("image"); a.add_argument("audio"); a.add_argument("query")
    a.add_argument("-o", "--out", default="avatar.mp4")

    sub.add_parser("health", help="префлайт: жив ли сервис")

    a = sub.add_parser("status", help="статус задачи"); a.add_argument("task_id")

    a = sub.add_parser("result", help="результат задачи")
    a.add_argument("task_id"); a.add_argument("-o", "--out", default="out.bin")

    for name in ("t2i", "i2i", "superres", "t2v", "i2v", "avatar"):
        sp = sub.choices[name]
        sp.add_argument("--no-censor", action="store_true", help="отключить цензуру")
    for name in sub.choices:
        sub.choices[name].add_argument(
            "--allow-insecure", action="store_true",
            help="разрешить plain HTTP в публичной сети (небезопасно)")
    return p


def main(argv=None):
    args = _build_parser().parse_args(argv)
    c = KandinskyClient(allow_insecure=getattr(args, "allow_insecure", False))
    censor = not getattr(args, "no_censor", False)
    cmd = args.cmd

    if cmd == "health":
        print(c.health()); return
    if cmd == "t2i":
        out = c.generate_image(args.query, resolution=args.resolution,
                               beautificator=args.beautificator, censor=censor, out=args.out)
    elif cmd == "i2i":
        out = c.edit_image(args.image, args.query, beautificator=args.beautificator,
                           censor=censor, out=args.out)
    elif cmd == "superres":
        out = c.upscale(args.image, upscale=args.upscale, one_step_t=args.one_step_t,
                        censor=censor, out=args.out)
    elif cmd == "t2v":
        out = c.text_to_video(args.query, resolution=args.resolution, pro=args.pro,
                              beautificator=args.beautificator, censor=censor, out=args.out)
    elif cmd == "i2v":
        out = c.animate_image(args.image, args.query, quality=args.quality,
                              beautificator=args.beautificator, censor=censor, out=args.out)
    elif cmd == "avatar":
        out = c.avatar(args.image, args.audio, args.query, censor=censor, out=args.out)
    elif cmd == "status":
        print(c.status(args.task_id)); return
    elif cmd == "result":
        out = c.result(args.task_id, out=args.out)
    else:
        raise KandinskyError(f"Неизвестная команда: {cmd}")

    print(f"Готово: {out}")


if __name__ == "__main__":
    try:
        main()
    except KandinskyError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
