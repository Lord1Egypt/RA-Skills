---
name: gua
description: 梅花易数起卦，根据上卦、下卦数字查六十四卦，给出卦名、动爻及详解链接。用法：/gua <上卦数> <下卦数>
---

## 起卦参数
用户传入的参数：$ARGUMENTS

## 起卦计算结果
!`python3 scripts/gua.py "$ARGUMENTS"`

---

## 输出说明

请根据以上计算结果，以如下格式输出：

```
上卦：[上卦名]（[象征]）
下卦：[下卦名]（[象征]）
本卦：[卦名]
动爻：[爻名]
详解：[URL]
```

然后用通俗中文简要解读此卦核心寓意（2-3句），结合动爻给出具体指引。

---

## 参考资料
- 八卦对照：[references/bagua.md](references/bagua.md)
- 时辰对照：[references/shichen.md](references/shichen.md)
- 六十四卦速查：[assets/64gua_table.md](assets/64gua_table.md)
- 卦意链接来源：[references/guas.json](references/guas.json)
