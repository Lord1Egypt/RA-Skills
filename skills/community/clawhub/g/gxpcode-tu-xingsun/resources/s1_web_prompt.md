# GxpCode-制药法规跟踪 — S1-Web 检测 Prompt

## 执行

```bash
python "${SKILL_DIR}/scripts/step1_web.py" resources/sources.yaml gxpcode_data
```

`step1_web.py` 读 `sources.yaml` 中 `type: web` 的源，用浏览器自动化打开列表页，按 `extract` 配置提取条目。

## 输出

`gxpcode_data/s1/s1_{name}.json`，每个 web 源一个文件。
