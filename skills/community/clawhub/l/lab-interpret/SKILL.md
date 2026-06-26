# Clinical Laboratory Report Interpreter

Interpret clinical lab results, identify abnormalities, and provide clinical context. Does not replace clinical judgment.

## Normal Reference Ranges (Adult)

| Test | Abbreviation | Normal Range | Unit |
| --- | --- | --- | --- |
| 白细胞 | WBC | 3.5–9.5 | ×10⁹/L |
| 红细胞 | RBC | 男 4.3–5.8 / 女 3.8–5.1 | ×10¹²/L |
| 血红蛋白 | HGB | 男 130–175 / 女 115–150 | g/L |
| 血小板 | PLT | 125–350 | ×10⁹/L |
| 空腹血糖 | FBG | 3.9–6.1 | mmol/L |
| 肌酐 | Cr | 男 57–111 / 女 41–81 | μmol/L |
| 谷丙转氨酶 | ALT | 9–50 | U/L |
| 谷草转氨酶 | AST | 15–40 | U/L |
| 甘油三酯 | TG | 0.28–1.80 | mmol/L |
| 总胆固醇 | TC | 2.85–5.70 | mmol/L |
| 促甲状腺激素 | TSH | 0.27–4.2 | mIU/L |
| CEA | CEA | < 5.0 | μg/L |
| AFP | AFP | < 20 | μg/L |
| CA125 | CA125 | < 35 | kU/L |
| CA19-9 | CA19-9 | < 35 | kU/L |

## Critical Values (危急值)

| 项目 | 危急值 | 处理 |
| --- | --- | --- |
| WBC | < 2.0 或 > 30.0 | 立即复查 |
| K⁺ | < 2.8 或 > 6.5 mmol/L | 心律失常风险 |
| Na⁺ | < 120 或 > 160 mmol/L | 神经系统症状 |
| cTnI/cTnT | 阳性/升高 | 急性心梗 |

## Usage

Triggered by: `解读检验`, `检验报告`, `血常规解读`, `生化解读`, `肝肾功能`, `甲功`, `血脂`, `血糖`, `肿瘤标志物`