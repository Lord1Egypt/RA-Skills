#!/bin/bash
# 词条表 · 英文 · 公共（多个脚本都用的短句）
# ⚠️ 值里的 % 都要写成 %%，整串是 printf 的格式串。

M_LANG_PROMPT="Language / 语言   [1] English   [2] 中文   (default 1): "
M_LANG_SAVED="Language set to %s — change any time with --lang zh / HKW_LANG=zh"
M_LANG_CURRENT="language: %s"
M_LANG_UNKNOWN="unknown language '%s', falling back to English"

M_PKG_OK="✓ %s"
M_PKG_SKIP="%s already installed, skipped"
M_YES_NO="[y/N] "
M_SKIPPED="· skipped"
M_DONE_EXEC="✓ done"
M_FAILED_EXEC="✗ failed — please run it by hand"
