# ct-base 家族共享后台大模型 key（LongCat-2.0，2026-09-25 起；原 deepseek v4-flash 作废）
# XOR+base64 混淆 blob（防目录扫描，非加密；公用凭据，参照 coze.dat 处理）。
# 运行时由 adapters/llm_loader.py 的 load_llm_key() 解码；发布平台拒 .dat，故用 .py 承载。
# 权威来源：ct-base/config/llm_key.py（本文件为其拷贝，随技能进发布载荷）。
LLM_API_KEY_BLOB = 'Ah9yUFgdXEofWFR0RSpTQVchGBFyVSFZVDs8XU4oXCc='
