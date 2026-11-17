# Determinism 幂等性保证详情

## 输入指纹（缓存 key）

决定输出的确定性关键字段：
```
用户身份: {融资阶段, 经验, 风格偏好}
用户提问: {具体问题内容}
触发模块: {诊断/材料/雷达/谈判/尽调/情绪}
```

**相同 {身份 + 提问 + 模块} → 相同输出**。可作为缓存 key：

- **脚本评分** → Hash=MD5({traction,market,team,product,story,unit_econ,use_funds,timing})，命中直接返回
- **TS 条款分析** → Hash=MD5({clause_name + clause_value})，命中直接返回
- **情绪支持话术** → LLM生成（建议temperature=0.3）
- **诊断报告** → 建议缓存24小时
