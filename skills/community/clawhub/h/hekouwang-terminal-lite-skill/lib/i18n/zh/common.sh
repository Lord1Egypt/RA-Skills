#!/bin/bash
# 词条表 · 中文 · 公共
# ⚠️ 只写「跟英文不一样」的条目也行：en 先加载打底，这里覆盖。

M_LANG_PROMPT="语言 / Language   [1] English   [2] 中文   （默认 1）："
M_LANG_SAVED="语言已设为 %s —— 随时可改：--lang en / HKW_LANG=en"
M_LANG_CURRENT="语言：%s"
M_LANG_UNKNOWN="认不出语言 '%s'，回落到英文"

M_PKG_OK="✓ %s"
M_PKG_SKIP="%s 已装，跳过"
M_YES_NO="[y/N] "
M_SKIPPED="· 跳过"
M_DONE_EXEC="✓ 已执行"
M_FAILED_EXEC="✗ 执行失败，请手动跑"
