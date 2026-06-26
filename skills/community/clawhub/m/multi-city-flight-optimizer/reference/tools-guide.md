# 工具使用指南

## ask_user_question 工具

用于收集用户出行约束的交互式提问工具。

**调用格式**：
```json
{
  "questions": [
    {
      "question": "问题内容？",
      "header": "短标签（最多12字符）",
      "options": [
        { "label": "选项1", "description": "选项说明" },
        { "label": "选项2", "description": "选项说明" }
      ],
      "multiSelect": false
    }
  ]
}
```

**使用场景**：
- 收集出发城市、假期时间窗、候选城市
- 确认中转偏好、舱位偏好
- 让用户选择 Top 方案
- 收紧偏好（再便宜/再省时）
- 确认候选城市列表（多选）

**注意事项**：
- 每次最多问 4 个问题
- 系统自动添加"其他"选项供用户自由输入
- 优先使用 Memory 中的已知信息，减少重复追问
- 候选城市收集时使用 `multiSelect: true`

---

## FlyAI 核心能力

本技能主要使用以下搜索命令：

| 命令 | 用途 | 在本场景中的作用 |
|------|------|------------------|
| `search-flight` | 机票搜索 | **核心**：搜索去程/回程每条航线 |
| `keyword-search` | 自然语言搜索 | **辅助**：搜索城市别名、替代机场 |

> ⚠️ **SSL 证书问题**：所有命令前加 `NODE_TLS_REJECT_UNAUTHORIZED=0`

**调用示例**：
```bash
# 去程搜索：出发地→候选城市
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "巴塞罗那" \
  --dep-date-start 2026-10-01 --dep-date-end 2026-10-02 \
  --sort-type 3

# 回程搜索：候选城市→出发地
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "里斯本" --destination "杭州" \
  --dep-date-start 2026-10-06 --dep-date-end 2026-10-07 \
  --sort-type 3

# 自然语言搜索（辅助）
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search \
  --query "杭州飞南欧 国庆 机票"
```

---

## 搜索策略

### 并行搜索

当候选城市有多个时，**并行发起**所有去程和回程搜索以减少等待时间：

```
候选城市 = [巴塞罗那, 马德里, 里斯本]

并行任务：
  Task 1: 杭州 → 巴塞罗那（去程）
  Task 2: 杭州 → 马德里（去程）
  Task 3: 杭州 → 里斯本（去程）
  Task 4: 巴塞罗那 → 杭州（回程）
  Task 5: 马德里 → 杭州（回程）
  Task 6: 里斯本 → 杭州（回程）
```

### 城市名称兼容

国际城市可能需要尝试多种名称：

| 中文 | 英文 | IATA码 |
|------|------|--------|
| 巴塞罗那 | Barcelona | BCN |
| 马德里 | Madrid | MAD |
| 里斯本 | Lisbon | LIS |
| 罗马 | Rome | FCO/CIA |
| 哥本哈根 | Copenhagen | CPH |
| 斯德哥尔摩 | Stockholm | ARN |
| 布宜诺斯艾利斯 | Buenos Aires | EZE |

**搜索降级策略**：
1. 先用中文名搜索
2. 搜不到则用英文名
3. 再搜不到则用 IATA 码
4. 全部失败则标注"暂无航线"并通知用户

### 多排序策略

根据用户偏好，使用不同排序方式搜索：

| 用户偏好 | 搜索排序 | sort-type |
|---------|---------|-----------|
| 综合最优 | 价格升序 + 时长升序各搜一次 | 3 + 4 |
| 最省钱 | 价格升序 | 3 |
| 最省时 | 时长升序 | 4 |
| 最稳妥 | 直飞优先 | 8 |

---

## fetch_content 工具

用于获取目的地相关的补充信息：

```python
fetch_content(url="[目的地信息链接]", query="签证 天气 交通")
```

**使用场景**：
- 查询申根签证要求
- 查询目的地当季天气
- 查询城际交通方式和时刻

---

## create_file 工具

用于生成 HTML 可视化方案文件：

```python
create_file(
  file_path="[用户工作目录]/航线比价-[出发城市]-[区域]-[出发日期].html",
  file_content="[HTML内容]"
)
```

**文件命名规则**：`航线比价-{出发城市}-{区域}-{出发日期}.html`
- 示例：`航线比价-杭州-南欧-2026-10-01.html`
