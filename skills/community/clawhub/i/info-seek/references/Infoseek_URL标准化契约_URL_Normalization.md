# Infoseek URL 标准化契约

> 版本：v1.0.1 ｜ 状态：✅ 已提供 ｜ 对齐全：`scripts/infoseek_helper.py::normalize_url`

## 1. 7 条规则（按序执行）

```
输入 URL
  ① 协议归一   http → https（http/https 之外保持原样）
  ② www 剥离   netloc 去除 www. 前缀
  ③ 域名小写   netloc 整体 lower()
  ④ 尾部斜杠   path 非 "/" 时去除末尾 "/"
  ⑤ UTM 剥离   移除跟踪参数（见白名单）
  ⑥ 参数排序   query 按 key 字母序重排（保证哈希一致）
  ⑦ Fragment 剥离  丢弃 #fragment
输出 标准化 URL
```

## 2. UTM 参数白名单

```
utm_source  utm_medium  utm_campaign  utm_term  utm_content
fbclid  gclid  msclkid  mc_cid  mc_eid
ref  source  _hsenc  _hsmi  hsCtaTracking
```

## 3. 去重键

```
dedup_key = sha1(normalize_url(url))
```

- 相同内容不同跟踪参数 → 同键去重
- 大小写/协议差异 → 同键去重

## 4. 边界行为

| 输入 | 行为 |
|------|------|
| 空串 / None | 原样返回（不崩溃） |
| 无协议（example.com/x） | scheme 空 → 保持原样 |
| 已标准化 URL | 幂等（重复调用结果不变） |

## 5. 兼容性

- 新增跟踪参数需同步 UTM_PARAMS 白名单
- 规则变更须保证幂等性（normalize(normalize(x)) == normalize(x)）
