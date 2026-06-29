#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global Auto Translator - 跨境电商外贸智能翻译引擎
专为跨境电商、外贸出海打造的智能翻译守护进程
"""

import os
import sys
import json
import time
import subprocess
import hashlib
import re

try:
    from langdetect import detect, LangDetectException
except ImportError:
    print("缺少 langdetect，运行: pip3 install langdetect")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("缺少 requests，运行: pip3 install requests")
    sys.exit(1)

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.expanduser("~/.openclaw/global-auto-translator")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
TERMS_PATH = os.path.join(CONFIG_DIR, "custom-terms.json")
PID_FILE = os.path.join(CONFIG_DIR, "daemon.pid")
STATE_FILE = os.path.join(CONFIG_DIR, "state.json")

LANG_NAMES = {
    "zh": "中文", "zh-cn": "简体中文", "zh-tw": "繁体中文",
    "en": "英文", "ja": "日文", "ko": "韩文",
    "fr": "法文", "de": "德文", "es": "西班牙文",
    "ru": "俄文", "ar": "阿拉伯文", "pt": "葡萄牙文",
    "it": "意大利文", "nl": "荷兰文", "sv": "瑞典文",
    "pl": "波兰文", "tr": "土耳其文", "th": "泰文",
    "vi": "越南文", "id": "印尼文", "hi": "印地文",
    "uk": "乌克兰文", "cs": "捷克文", "da": "丹麦文",
    "el": "希腊文", "he": "希伯来文", "hu": "匈牙利文",
    "ro": "罗马尼亚文", "sk": "斯洛伐克文", "bg": "保加利亚文",
    "fi": "芬兰文", "no": "挪威文", "ca": "加泰罗尼亚文",
    "hr": "克罗地亚文", "lt": "立陶宛文", "lv": "拉脱维亚文",
    "et": "爱沙尼亚文", "sl": "斯洛文尼亚文", "sr": "塞尔维亚文",
    "ms": "马来文", "tl": "菲律宾文", "bn": "孟加拉文",
    "ta": "泰米尔文", "ur": "乌尔都文", "fa": "波斯文",
    "sw": "斯瓦希里文", "af": "南非荷兰文", "is": "冰岛文",
    "ga": "爱尔兰文", "cy": "威尔士文", "mk": "马其顿文",
    "be": "白俄罗斯文", "ka": "格鲁吉亚文",
}


def load_config():
    default = {
        "target_language": "zh",
        "poll_interval": 2,
        "min_text_length": 3,
        "translation_service": "mymemory",
        "sound_alert": True,
        "copy_to_clipboard": True,
        "excluded_apps": [],
        "trade_terms_enabled": True,
        "preserve_formatting": True,
        "prompt_cooldown": 30,
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
                default.update(cfg)
        except Exception:
            pass
    return default


def load_trade_terms():
    if os.path.exists(TERMS_PATH):
        try:
            with open(TERMS_PATH) as f:
                data = json.load(f)
                return data.get("trade_terms", {})
        except Exception:
            pass
    return {}


def find_trade_terms(text, terms):
    """从文本中找出匹配的外贸术语"""
    if not terms:
        return {}
    found = {}
    for term, meaning in sorted(terms.items(), key=lambda x: len(x[0]), reverse=True):
        # 使用单词边界匹配，避免部分匹配
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        if pattern.search(text):
            found[term] = meaning
    return found


def append_trade_glossary(translated, found_terms):
    """翻译后：附加术语对照表"""
    if not found_terms:
        return translated
    glossary_lines = ["", "--- 外贸术语对照 ---"]
    for term, meaning in found_terms.items():
        glossary_lines.append("  %s: %s" % (term, meaning))
    return translated + "\n".join(glossary_lines)


def save_state(clipboard_hash="", last_text="", last_lang=""):
    state = {
        "clipboard_hash": clipboard_hash,
        "last_text": last_text[:200] if last_text else "",
        "last_lang": last_lang,
        "last_prompt_time": time.time(),
    }
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"clipboard_hash": "", "last_prompt_time": 0}


def get_clipboard():
    try:
        result = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=2)
        return result.stdout.strip()
    except Exception:
        return ""


def set_clipboard(text):
    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
        proc.communicate(input=text)
    except Exception:
        pass


def detect_language(text):
    if len(text) < 5 and text.isascii():
        return "en"
    try:
        lang = detect(text)
        # 过短文本的误判修正
        if len(text) < 30:
            # 纯英文字母或常见英文短语
            if lang in ("nl", "no", "da", "sv") and text.lower() in (
                "hello world", "hello", "hi", "test", "hello world, how are you",
                "good morning", "good afternoon", "good evening", "thank you",
                "please", "yes", "no", "ok", "thanks",
            ):
                return "en"
        return lang
    except LangDetectException:
        return None


def is_foreign_text(text, target_lang):
    if not text or len(text) < 3:
        return False
    detected = detect_language(text)
    if detected is None:
        return False
    if target_lang.startswith("zh") and detected in ("zh-cn", "zh-tw", "zh"):
        return False
    if detected.startswith(target_lang):
        return False
    return True


def translate_mymemory(text, target="zh"):
    try:
        source_lang = detect_language(text) or "en"
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text[:4500], "langpair": f"{source_lang}|{target}"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("responseStatus") == 200:
            translated = data["responseData"]["translatedText"]
            matches = data.get("matches", [])
            if matches:
                best = max(matches, key=lambda m: m.get("match", 0))
                best_translation = best.get("translation", "")
                if best_translation and best_translation != text[:len(best_translation)]:
                    translated = best_translation
                best_src = best.get("source", source_lang)
                if best_src:
                    source_lang = best_src.split("-")[0]
            return translated, source_lang
        return None, None
    except Exception:
        return None, None


def translate_youdao(text, target="zh"):
    try:
        url = "https://dict.youdao.com/jsonapi"
        params = {"q": text[:2000], "keyfrom": "fanyi.web", "doctype": "json", "type": "data"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://fanyi.youdao.com/"
        }
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        web_trans = data.get("web_trans", {}).get("web-translation", [])
        if web_trans and web_trans[0].get("trans"):
            trans_list = web_trans[0]["trans"]
            if trans_list:
                translated = trans_list[0].get("value", "")
                if translated:
                    return translated, "en"
        ec = data.get("ec", {}).get("word", {})
        if ec and ec.get("trs"):
            words = []
            for tr in ec["trs"][:3]:
                if tr.get("tr") and tr["tr"][0].get("l", {}).get("i"):
                    words.append(tr["tr"][0]["l"]["i"])
            if words:
                return " ".join(words), "en"
        return None, None
    except Exception:
        return None, None


def translate_deepl(text, target, config):
    try:
        url = "https://api-free.deepl.com/v2/translate"
        dl_target = "zh" if target.startswith("zh") else target
        resp = requests.post(url, data={"text": text[:5000], "target_lang": dl_target.upper()},
                            headers={"Authorization": "DeepL-Auth-Key " + config.get("deepl_api_key", "")}, timeout=10)
        data = resp.json()
        return data["translations"][0]["text"], target
    except Exception:
        return None, None


def translate_text(text, config):
    service = config.get("translation_service", "mymemory")
    target = config.get("target_language", "zh")
    if service == "deepl" and config.get("deepl_api_key"):
        result = translate_deepl(text, target, config)
        if result[0]:
            return result
    result = translate_mymemory(text, target)
    if result[0]:
        return result
    result = translate_youdao(text, target)
    if result[0]:
        return result
    return None, None


def show_dialog(title, message, buttons=None, default=0, cancel=1):
    if buttons is None:
        buttons = ["是的，翻译", "不用了"]
    button_list = 'buttons {"%s"}' % '", "'.join(buttons)
    default_btn = "default button %d" % (default + 1)
    cancel_btn = "cancel button %d" % (cancel + 1)
    escaped_msg = message.replace('"', '\\"').replace('\n', '\\n')
    escaped_title = title.replace('"', '\\"')
    script = 'display dialog "%s" with title "%s" %s %s %s\nbutton returned of result' % (
        escaped_msg, escaped_title, button_list, default_btn, cancel_btn)
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except Exception:
        return None


def show_translation_result(translated, source_lang):
    lang_name = LANG_NAMES.get(source_lang, source_lang)
    target_name = LANG_NAMES.get(load_config().get("target_language", "zh"), "中文")
    display_text = translated if len(translated) <= 1500 else translated[:1500] + "..."
    escaped_text = display_text.replace('"', '\\"')
    title = "翻译完成 (%s -> %s)" % (lang_name, target_name)
    escaped_title = title.replace('"', '\\"')
    script = 'set theText to "%s"\ndisplay dialog theText with title "%s" with icon note buttons {"复制到剪贴板", "关闭"} default button 1\nbutton returned of result' % (
        escaped_text, escaped_title)
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except Exception:
        return None


def play_sound():
    try:
        subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], capture_output=True, timeout=3)
    except Exception:
        pass


def get_active_app():
    try:
        result = subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to get name of first application process whose frontmost is true'],
            capture_output=True, text=True, timeout=2)
        return result.stdout.strip()
    except Exception:
        return ""


def run_daemon():
    config = load_config()
    poll_interval = config.get("poll_interval", 2)
    min_length = config.get("min_text_length", 3)
    target_lang = config.get("target_language", "zh")
    prompt_cooldown = config.get("prompt_cooldown", 30)
    trade_terms_enabled = config.get("trade_terms_enabled", True)
    terms = load_trade_terms() if trade_terms_enabled else {}
    terms_count = len(terms)

    print("Global Auto Translator 已启动")
    print("监控剪贴板 | 目标语言: %s" % LANG_NAMES.get(target_lang, target_lang))
    print("翻译引擎: MyMemory + 有道(备用)")
    if terms_count > 0:
        print("外贸术语库: %d 条术语已加载" % terms_count)
    print("轮询间隔: %d秒 | 冷却: %d秒" % (poll_interval, prompt_cooldown))
    print("按 Ctrl+C 停止\n")

    try:
        while True:
            time.sleep(poll_interval)
            text = get_clipboard()
            if not text or len(text) < min_length:
                continue
            text_hash = hashlib.md5(text.encode()).hexdigest()
            state = load_state()
            if text_hash == state.get("clipboard_hash", ""):
                continue
            if time.time() - state.get("last_prompt_time", 0) < prompt_cooldown:
                continue
            if not is_foreign_text(text, target_lang):
                save_state(text_hash, text, detect_language(text) or "")
                continue
            active_app = get_active_app()
            excluded = config.get("excluded_apps", [])
            if active_app in excluded:
                save_state(text_hash, text, "")
                continue
            detected_lang = detect_language(text) or "unknown"
            lang_name = LANG_NAMES.get(detected_lang, detected_lang)
            print("检测到%s内容 (来自: %s)" % (lang_name, active_app))
            if config.get("sound_alert"):
                play_sound()
            # 术语预处理
            found_terms = find_trade_terms(text, terms)
            dialog_msg = "检测到%s内容:\n\n%s\n\n是否需要翻译？" % (lang_name, text[:150] + ("..." if len(text) > 150 else ""))
            result = show_dialog("翻译助手", dialog_msg, buttons=["是的，翻译", "不用了"])
            if result and ("翻译" in result or "Yes" in result):
                translated, src_lang = translate_text(text, config)
                if translated:
                    translated = append_trade_glossary(translated, found_terms)
                    action = show_translation_result(translated, src_lang)
                    if action and ("复制" in action or "copy" in action.lower()):
                        set_clipboard(translated)
                        print("译文已复制: %s..." % translated[:60])
                    else:
                        print("翻译完成: %s..." % translated[:80])
                    save_state(text_hash, text, detected_lang)
                else:
                    print("翻译失败")
                    show_dialog("翻译失败", "翻译服务暂不可用，请稍后再试。")
            else:
                print("跳过翻译")
                save_state(text_hash, text, detected_lang)
    except KeyboardInterrupt:
        print("\n守护进程已停止")


def cmd_start():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            old_pid = f.read().strip()
        try:
            os.kill(int(old_pid), 0)
            print("守护进程已在运行 (PID: %s)" % old_pid)
            return
        except OSError:
            pass
    pid = os.fork()
    if pid == 0:
        os.setsid()
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
        os.chdir(CONFIG_DIR)
        sys.stdout = open(os.path.join(CONFIG_DIR, "daemon.log"), "a")
        sys.stderr = sys.stdout
        run_daemon()
    else:
        print("守护进程已启动 (PID: %d)" % pid)
        with open(PID_FILE, "w") as f:
            f.write(str(pid))


def cmd_stop():
    if not os.path.exists(PID_FILE):
        print("守护进程未运行")
        return
    with open(PID_FILE) as f:
        pid = f.read().strip()
    try:
        os.kill(int(pid), 9)
        print("守护进程已停止 (PID: %s)" % pid)
    except OSError:
        print("进程已不存在")
    finally:
        try:
            os.remove(PID_FILE)
        except OSError:
            pass


def cmd_status():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = f.read().strip()
        try:
            os.kill(int(pid), 0)
            print("守护进程运行中 (PID: %s)" % pid)
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE) as f:
                    state = json.load(f)
                last_time = state.get("last_prompt_time", 0)
                if last_time:
                    ago = int(time.time() - last_time)
                    lang = state.get("last_lang", "?")
                    print("上次检测: %d秒前 | 语言: %s" % (ago, lang))
        except OSError:
            print("守护进程未运行 (残留PID文件)")
            try:
                os.remove(PID_FILE)
            except OSError:
                pass
    else:
        print("守护进程未运行")


def cmd_translate():
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
        if text:
            config = load_config()
            tgt = config.get("target_language", "zh")
            tgt_name = LANG_NAMES.get(tgt, tgt)
            terms_enabled = config.get("trade_terms_enabled", True)
            terms = load_trade_terms() if terms_enabled else {}
            found_terms = find_trade_terms(text, terms)
            translated, src_lang = translate_text(text, config)
            if translated:
                translated = append_trade_glossary(translated, found_terms)
                src_name = LANG_NAMES.get(src_lang, src_lang)
                print("[%s] -> [%s]" % (src_name, tgt_name))
                print(translated)
            else:
                print("翻译失败", file=sys.stderr)
                sys.exit(1)
        return
    else:
        print("用法: echo '文本' | translate-daemon.py translate")
        sys.exit(1)


if __name__ == "__main__":
    cmd_map = {
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "translate": cmd_translate,
    }
    if len(sys.argv) > 1 and sys.argv[1] in cmd_map:
        cmd_map[sys.argv[1]]()
    else:
        print("Global Auto Translator - 跨境电商外贸智能翻译引擎")
        print()
        print("用法:")
        print("  python3 translate-daemon.py start      启动守护进程")
        print("  python3 translate-daemon.py stop       停止守护进程")
        print("  python3 translate-daemon.py status     查看状态")
        print("  echo '文本' | translate-daemon.py translate  手动翻译")
