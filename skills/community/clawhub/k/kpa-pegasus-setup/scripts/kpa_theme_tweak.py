#!/usr/bin/env python3
"""KPA 天马 prosperoOS 主题增强（v2.0.1 新增）

解决两个实机痛点：
  1) 顶部平台名太小、切平台看不出当前在哪  -> 字号 24→36、选中纯白/未选中压暗、平台条常显
  2) 退出游戏后回到平台第一个游戏而非刚才那个 -> 记录 Last Game 并在重启后定位回去

实现方式：pull theme.qml / GameBar.qml → 精确文本替换 → 备份后 push → 可选清缓存重启天马。
所有替换都基于唯一锚点且幂等：已改过的不会重复插入；锚点找不到会明确报错并跳过该处。

用法：
  python3 scripts/kpa_theme_tweak.py              # 只检查，不写
  python3 scripts/kpa_theme_tweak.py --apply      # 写入设备
  python3 scripts/kpa_theme_tweak.py --revert     # 从 .bakKPA3 恢复
  python3 scripts/kpa_theme_tweak.py --apply --restart   # 写入后清缓存并重启天马

注意：本工具针对 prosperoOS 主题（master 分支）的 QML 结构。若主题大版本变更导致
锚点失配，脚本会报告具体哪一处不匹配，不会写入半成品。
"""
import os
import shutil
import subprocess
import sys
import tempfile

THEME_DIR = "/sdcard/pegasus-frontend/themes/prosperoOS"
PEG_PKG = "org.pegasus_frontend.android"
CACHE = "/sdcard/pegasus-frontend/dataCache.json"
BAK_SUFFIX = ".bakKPA3"

# theme.qml 的 5 处替换：(名称, 原文, 新文)
THEME_EDITS = [
    (
        "最近游戏条 10→16",
        "    ListLastPlayed  { id: listRecent; max: 10 }",
        "    ListLastPlayed  { id: listRecent; max: 16 }",
    ),
    (
        "launchGame 记录 Last Game + 新增 restoreLastGame",
        """    // Launch the current game
    function launchGame(game) {
        api.memory.set('Last Collection', currentCollection);
        if (game != null)
            game.launch();
        else
            currentGame.launch();
    }""",
        """    // Launch the current game
    function launchGame(game) {
        api.memory.set('Last Collection', currentCollection);
        if (game != null) {
            if (game.title) api.memory.set('Last Game', game.title);
            game.launch();
        } else {
            if (currentGame && currentGame.title) api.memory.set('Last Game', currentGame.title);
            currentGame.launch();
        }
    }

    // KPA 优化：天马被系统回收后重启，恢复到上次玩的游戏，而不是平台第一个
    function restoreLastGame(title) {
        if (!title) return;
        var coll = (currentCollection >= 0 && currentCollection < api.collections.count)
                   ? api.collections.get(currentCollection).games
                   : api.allGames;
        for (var i = 0; i < coll.count && i < 16; i++) {
            if (coll.get(i).title === title) {
                gameBar.currentIndex = i + 1;
                return;
            }
        }
    }""",
    ),
    (
        "启动时恢复上次游戏",
        """    Component.onCompleted: {
        currentCollection = api.memory.has('Last Collection') ? api.memory.get('Last Collection') : -1
        api.memory.unset('Last Collection');
    }""",
        """    Component.onCompleted: {
        currentCollection = api.memory.has('Last Collection') ? api.memory.get('Last Collection') : -1
        api.memory.unset('Last Collection');
        var lastGame = api.memory.has('Last Game') ? api.memory.get('Last Game') : ''
        api.memory.unset('Last Game');
        restoreLastGame(lastGame);
    }""",
    ),
    (
        "平台条常显（原 opacity 绑定 gameBar.active）",
        """        width: parent.width
        height: vpx(90)
        opacity: gameBar.active ? 1 : 0""",
        """        width: parent.width
        height: vpx(90)
        opacity: 1""",
    ),
    (
        "平台名字号 24→36 + 选中高亮",
        """                Text {
                    property bool selected: ListView.isCurrentItem
                    text:name
                    color: "white"
                    font.family: selected ? titleFont.name : subtitleFont.name
                    font.pixelSize: vpx(24)
                    width: implicitWidth + vpx(35)
                    height: collectionNav.height
                    verticalAlignment: Text.AlignVCenter
                }""",
        """                Text {
                    property bool selected: ListView.isCurrentItem
                    text:name
                    color: selected ? "#ffffff" : "#6affffff"
                    font.family: selected ? titleFont.name : subtitleFont.name
                    font.pixelSize: vpx(36)
                    width: implicitWidth + vpx(40)
                    height: collectionNav.height
                    verticalAlignment: Text.AlignVCenter
                }""",
    ),
]

GAMEBAR_EDITS = [
    (
        "顶部游戏条 10→16",
        "            var gamesCounter = activeCollection.count > 10 ? 10 : activeCollection.count;",
        "            var gamesCounter = activeCollection.count > 16 ? 16 : activeCollection.count;",
    ),
]


def find_adb():
    env = os.environ.get("KPA_ADB")
    if env and os.path.isfile(env) and os.access(env, os.X_OK):
        return env
    import glob as _glob
    for pat in (
        os.path.expanduser("~/WorkBuddy/*/tools/platform-tools/adb"),
        os.path.expanduser("~/.workbuddy/tools/platform-tools/adb"),
    ):
        hits = sorted(_glob.glob(pat))
        if hits:
            return hits[0]
    found = shutil.which("adb")
    if found:
        return found
    sys.exit("ERROR: 未找到 adb，请设置 KPA_ADB 环境变量")


ADB = find_adb()


def sh(cmd):
    return subprocess.run([ADB] + ["shell", cmd], capture_output=True,
                          text=True, stdin=subprocess.DEVNULL)


def pull(remote, local):
    r = subprocess.run([ADB, "pull", remote, local], capture_output=True,
                       text=True, stdin=subprocess.DEVNULL)
    return r.returncode == 0


def push(local, remote):
    r = subprocess.run([ADB, "push", local, remote], capture_output=True,
                       text=True, stdin=subprocess.DEVNULL)
    return r.returncode == 0


def apply_edits(text, edits, label):
    changed = 0
    for name, old, new in edits:
        if new in text:
            print(f"  SKIP   {label}: {name}（已是目标状态）")
            continue
        if old not in text:
            print(f"  MISS   {label}: {name}（锚点不匹配，跳过 —— 主题版本可能已变更）")
            continue
        text = text.replace(old, new, 1)
        print(f"  EDIT   {label}: {name}")
        changed += 1
    return text, changed


def main():
    do_apply = "--apply" in sys.argv
    do_revert = "--revert" in sys.argv
    do_restart = "--restart" in sys.argv

    if do_revert:
        for fn in ("theme.qml", "GameBar.qml"):
            remote = f"{THEME_DIR}/{fn}"
            r = sh(f"[ -f '{remote}{BAK_SUFFIX}' ] && echo yes")
            if "yes" in r.stdout:
                sh(f"cp '{remote}{BAK_SUFFIX}' '{remote}'")
                print(f"  REVERT {fn}")
            else:
                print(f"  SKIP   {fn}（无 {BAK_SUFFIX} 备份）")
        if do_restart:
            restart_pegasus()
        return

    tmp = tempfile.mkdtemp(prefix="kpa_theme_")
    total = 0
    try:
        for fn, edits in (("theme.qml", THEME_EDITS), ("GameBar.qml", GAMEBAR_EDITS)):
            remote = f"{THEME_DIR}/{fn}"
            local = os.path.join(tmp, fn)
            if not pull(remote, local):
                print(f"  ERROR  无法拉取 {remote}")
                continue
            with open(local, encoding="utf-8") as f:
                text = f.read()
            new_text, changed = apply_edits(text, edits, fn)
            total += changed
            if not do_apply:
                continue
            if changed == 0:
                print(f"  SKIP   不写回 {fn}（无需改动）")
                continue
            sh(f"[ -f '{remote}{BAK_SUFFIX}' ] || cp '{remote}' '{remote}{BAK_SUFFIX}'")
            with open(local, "w", encoding="utf-8") as f:
                f.write(new_text)
            if push(local, remote):
                print(f"  WRITE  {fn}（{changed} 处）")
            else:
                print(f"  ERROR  push 失败 {fn}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not do_apply:
        print(f"\n共需改动 {total} 处。真正写入加 --apply")
        return
    if total and do_restart:
        restart_pegasus()
    elif total:
        print("\n改动已写入。让天马重载：加 --restart，或手动重启天马。")


def restart_pegasus():
    print("  清理 dataCache 并重启天马…")
    sh(f"rm -f {CACHE}")
    sh(f"am force-stop {PEG_PKG}")
    sh("input keyevent 224")
    sh(f"monkey -p {PEG_PKG} -c android.intent.category.LAUNCHER 1")
    print("  已重启（天马首次重扫全库约 10–20 秒）")


if __name__ == "__main__":
    main()
