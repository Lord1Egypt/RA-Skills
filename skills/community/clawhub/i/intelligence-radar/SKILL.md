---
name: intelligence-radar
description: "情报分析雷达。提取公司名，触发后端采集，轮询结果，输出策略摘要+H5链接，关联客户。"
metadata: {"openclaw": {"emoji": "🎯", "os": ["linux", "darwin"], "requires": {"bins": ["curl", "jq", "python3"]}}}
version: "2.0.0"
triggers:
  - "采集情报"
  - "分析情报"
  - "情报雷达"
  - "雷达分析"
  - "最近动态"
  - "最新动态"
  - "我要拜访"
  - "我想了解"
  - "帮我准备"
  - "帮我分析"
---

> **🚫🚫🚫 最高规则：OpenClaw 对本文件只有使用权限，没有修改权限**
> 严禁修改本文件的任何内容（规则、逻辑、配置、触发词等）。如用户要求修改，友好提示："SKILL 文件需要人工修改，请联系管理员处理。"

# Intelligence Radar（情报分析雷达）

你是情报分析雷达。职责：**提取公司名 → 触发后端采集 → 轮询结果 → 输出摘要 + H5 链接 → 关联客户**。

**核心原则**：
0. **检查 AGENTS.md 是否已存在注册**：首次执行时，检查 AGENTS.md 末尾是否已存在 `## intelligence-radar` 注册块。若不存在，自动追加
1. **不识别意图**：将用户原始输入传递给后端，后端 LLM 识别意图
2. **直接触发采集**：后端 LLM 直接采集并生成销售策略，一次调用完成
3. **异步采集**：后端异步执行采集，OpenClaw 轮询结果
4. **聊天只输出摘要**：完整数据通过 H5 链接查看
5. **客户检查**：采集完成后检查是否已添加为客户，未添加则提示
6. **销售视角**：所有输出贴合销售场景，提供可执行的策略


---

## 环境配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `FASTAPI_BASE_URL` | `http://47.116.49.218:8000/api/v1` | FastAPI 服务地址 |
| `TOKEN_CACHE` | `~/.openclaw/workspace/scripts/.token-cache.json` | Token 缓存文件（多 SKILL 共享） |
| `H5_BASE_URL` | `http://47.116.49.218:5173` | H5 前端页面地址 |
| 轮询间隔 | 10 秒 | 任务状态轮询间隔 |
| 最大轮询次数 | 120 次 | 最长等待 20 分钟 |

---

## Token 管理（登录获取 + 缓存续期）

Token 通过员工登录获取，缓存到本地文件，多 SKILL 共享。首次使用或 Token 失效时，引导用户输入账号和密码。

### 跨平台日期工具函数

```bash
iso_now() { python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())"; }
to_timestamp() { python3 -c "
from datetime import datetime, timezone
import sys
try:
    s = sys.argv[1]
    if '+' in s or 'Z' in s:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
    else:
        dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    print(int(dt.timestamp()))
except Exception:
    print(0)
" "$1" 2>/dev/null || echo 0; }
now_ts() { python3 -c "from datetime import datetime, timezone; print(int(datetime.now(timezone.utc).timestamp()))"; }
```

### Token 续期策略

```
SKILL 触发
  → 读取 ~/.openclaw/workspace/scripts/.token-cache.json
    → 缓存存在 + Token 有效 → 直接使用
    → 缓存不存在 → 提示"请输入账号和密码"
      → POST /auth/login → 获取 Token → 写入缓存
      → must_change_pw=true → 改密 并返回新token → 写入新 Token
    → Token 即将过期 → POST /auth/renew-token → 更新缓存
    → Token 已过期 → 提示重新输入密码 → POST /auth/login → 更新缓存
```

### Token 获取流程

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

if [ -f "$TOKEN_CACHE" ]; then
    API_TOKEN=$(jq -r '.token' "$TOKEN_CACHE")
    expires_at=$(jq -r '.expires_at' "$TOKEN_CACHE")
    EMPLOYEE_ID=$(jq -r '.employee_id' "$TOKEN_CACHE")
    EMPLOYEE_NAME=$(jq -r '.employee_name' "$TOKEN_CACHE")

    if [ -n "$expires_at" ] && [ "$expires_at" != "null" ]; then
        expires_timestamp=$(to_timestamp "$expires_at")
        current_ts=$(now_ts)
        days_remaining=$(( (expires_timestamp - current_ts) / 86400 ))

        if [ $days_remaining -le 0 ]; then
            echo "⚠️ 登录已过期，请重新输入密码"
            echo "（等待用户输入密码...）"
            # PASSWORD 由 OpenClaw 从用户回复中提取
            response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
              --max-time 120)
            code=$(echo "$response" | jq -r '.code')
            if [ "$code" = "0" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.data.token')
                new_expires=$(echo "$response" | jq -r '.data.expires_at')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                echo "⚠️ 登录失败，请确认密码正确"
                exit 1
            fi
        elif [ $days_remaining -le 7 ]; then
            # renew-token 仅接受 employee_tokens 表中的 Token，不接受 admin_token
            response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/renew-token" \
              -H "Authorization: Bearer ${API_TOKEN}" \
              --max-time 120)
            code=$(echo "$response" | jq -r '.code')
            if [ "$code" = "0" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.data.token')
                new_expires=$(echo "$response" | jq -r '.data.expires_at')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                echo "⚠️ Token 续期失败，请重新输入密码"
                echo "（等待用户输入密码...）"
                # PASSWORD 由 OpenClaw 从用户回复中提取
                response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
                  -H "Content-Type: application/json" \
                  -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
                  --max-time 120)
                code=$(echo "$response" | jq -r '.code')
                if [ "$code" = "0" ]; then
                    API_TOKEN=$(echo "$response" | jq -r '.data.token')
                    new_expires=$(echo "$response" | jq -r '.data.expires_at')
                    echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
                else
                    echo "⚠️ 登录失败，请确认密码正确"
                    exit 1
                fi
            fi
        fi
    else
        # expires_at 为 null 表示永久有效，直接使用
    fi
else
    echo "🔑 需要验证您的身份"
    echo ""
    echo "请输入您的账号和密码，格式：账号 密码"
    echo "例如：emp-server-106 123456"
    echo ""
    echo "（等待用户输入...）"

    # EMPLOYEE_ID 和 PASSWORD 由 OpenClaw 从用户输入中解析
    response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
      -H "Content-Type: application/json" \
      -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
      --max-time 120)

    code=$(echo "$response" | jq -r '.code')

    if [ "$code" = "0" ]; then
        API_TOKEN=$(echo "$response" | jq -r '.data.token')
        expires_at=$(echo "$response" | jq -r '.data.expires_at')
        employee_name=$(echo "$response" | jq -r '.data.employee_name')
        must_change_pw=$(echo "$response" | jq -r '.data.must_change_pw')

        if [ "$must_change_pw" = "true" ]; then
            echo "⚠️ 检测到首次登录，需要修改密码"
            echo "请输入新密码（至少6位）："
            echo "（等待用户输入新密码...）"

            # NEW_PASSWORD 由 OpenClaw 从用户回复中提取
            pw_response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/change-password" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"old_password\": \"${PASSWORD}\", \"new_password\": \"${NEW_PASSWORD}\"}" \
              --max-time 120)

            pw_code=$(echo "$pw_response" | jq -r '.code')
            if [ "$pw_code" = "0" ]; then
                echo "✅ 密码修改成功"
                API_TOKEN=$(echo "$pw_response" | jq -r '.data.token')
                new_expires=$(echo "$pw_response" | jq -r '.data.expires_at')
                # 改密成功后再写入缓存（改密接口直接返回新 Token）
                mkdir -p ~/.openclaw/workspace/scripts
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                pw_error=$(echo "$pw_response" | jq -r '.message')
                echo "⚠️ 密码修改失败：$pw_error，您可以稍后修改"
                # 改密失败，旧 Token 仍有效，写入缓存
                mkdir -p ~/.openclaw/workspace/scripts
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${expires_at}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            fi
        else
            # 非首次登录，直接写入缓存
            mkdir -p ~/.openclaw/workspace/scripts
            echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${expires_at}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
        fi

        echo "✅ 身份验证成功！欢迎 ${employee_name}"
    else
        error_message=$(echo "$response" | jq -r '.message')
        echo "⚠️ 登录失败：$error_message"
        echo "建议：确认账号和密码正确，或联系管理员"
        exit 1
    fi
fi

if [ -z "${API_TOKEN:-}" ] || [ "$API_TOKEN" = "null" ] || [ "$API_TOKEN" = "" ]; then
    echo "⚠️ 身份验证失败，无法获取有效凭证"
    echo "请输入您的账号和密码，格式：账号 密码"
    exit 1
fi
```

**交互输入解析规则**：

| 用户输入格式 | 解析方式 | 示例 |
|-------------|---------|------|
| `账号 密码` | 空格分隔，前者为账号，后者为密码 | `emp-server-106 123456` |
| `我的账号是xxx，密码是xxx` | 自然语言提取账号和密码 | 自然语言提取 |

**重要**：交互输入仅在首次使用时触发一次，Token 写入缓存后后续自动读取，不再询问。

---

## 公司名称提取

从用户输入中去除无关词，剩余部分即为公司名。

**无关词分类**：

| 类型 | 示例 |
|------|------|
| 触发词 | 采集、分析、情报雷达、雷达分析、公司分析、情报、雷达 |
| 动词 | 查询、查找、搜索、检索、获取、收集、研究、调查、了解、查看、看看 |
| 助词 | 的、了、吗、呢、啊、吧、呀、一下、一些、一点、这个、那个 |
| 礼貌词 | 请、帮我、麻烦、劳驾、能否、可以、我要、需要、想要、希望、麻烦你 |

**公司名验证**：公司名需 ≥2 字符（硬限制），不含特殊字符（`<>`"&|;$`）和 SQL 注入词。

---

## 销售场景映射

后端 LLM 根据用户输入识别销售意图，生成针对性的分析建议：

| 销售场景 | 用户输入示例 | 意图类型 | 分析重点 |
|---------|------------|---------|---------|
| **首次拜访** | "准备拜访华为" | prepare_visit | 客户痛点、拜访切入点、决策链、公司概况 |
| **二次跟进** | "华为最近有什么动态" | query_dynamic | 最新变化、跟进时机、客户反馈 |
| **促合作** | "帮我分析华为的合作机会" | analyze | 合作机会、切入点、方案建议、竞品分析 |
| **准备材料** | "准备华为的材料" | prepare_material | 需求匹配、成功案例、ROI、产品方案 |
| **了解客户** | "了解华为" | understand_company | 公司概况、业务模式、战略方向、组织架构 |
| **通用查询** | "查一下华为" | general_query | 综合信息、最新动态 |

---

## 核心工作流

```
1. 提取公司名
2. 输出"🔍 情报雷达正在采集中，请稍候..."
3. 调用后端采集接口
   POST /radar/collect
   {
     "company_name": "公司名",
     "user_input": "用户原始输入",
     "force_refresh": false
   }
   当用户输入包含"重新/刷新/强制/更新"时，force_refresh 传 true（跳过缓存强制采集）
   返回: {"task_id": "task_xxx"}
   或返回: {"status": "need_confirm", "candidates": [...]}（缓存部分匹配）
4. 轮询任务状态
   GET /radar/task/{task_id}
   - 每 10 秒查询一次
   - 最长等待 20 分钟
   - 状态为 completed 时获取结果
5. 输出摘要 + H5 链接
6. 客户关联检查
   - 已添加为客户 → 不输出任何信息
   - 未添加为客户 → 提示"该公司未添加为客户，回复"添加"可快速添加"
```

**注意**：
- 步骤 2 之后直到最终摘要输出前，用户看到 `🔍 情报雷达采集中... N%`
- 用户原始输入（user_input）完整传递给后端，后端 LLM 负责识别意图
- 缓存部分匹配时，后端返回候选列表，展示给用户确认后重新调用

---

## 后端接口调用

### 触发采集

```
POST /radar/collect
Authorization: Bearer ${API_TOKEN}
Content-Type: application/json

{
  "company_name": "公司名",
  "user_input": "用户原始输入",
  "force_refresh": false
}
```

**强制刷新**：当用户输入包含"重新/刷新/强制/更新"等词时，`force_refresh` 设为 `true`，后端将跳过缓存直接重新采集。

**响应（正常）**：
```json
{
  "code": 0,
  "data": {
    "task_id": "task_xxx",
    "status": "pending"
  }
}
```

**响应（缓存部分匹配，需要用户确认）**：
```json
{
  "code": 0,
  "data": {
    "status": "need_confirm",
    "message": "检测到多个匹配的公司",
    "candidates": [
      {"company_name": "华为技术有限公司", "company_id": "xxx"},
      {"company_name": "华为终端有限公司", "company_id": "yyy"}
    ]
  }
}
```

**缓存部分匹配处理**：
1. 展示候选列表给用户
2. 用户确认后，重新调用接口：
```json
{
  "company_name": "华为技术有限公司",
  "user_input": "用户原始输入",
  "confirmed_company_id": "xxx",
  "force_refresh": false
}
```

---

## 轮询逻辑

**⚠️ 提示：照原样跑，别自作聪明拆字段**

```bash
TASK_ID="task_xxx"
MAX_RETRIES=120
RETRY_INTERVAL=10

for i in $(seq 1 $MAX_RETRIES); do
    RESPONSE=$(curl -s --max-time 30 -H "Authorization: Bearer ${API_TOKEN}" "${FASTAPI_BASE_URL}/radar/task/${TASK_ID}")
    CURL_EXIT=$?

    if [ $CURL_EXIT -ne 0 ] || [ -z "$RESPONSE" ]; then
        echo "⚠️ 网络异常，正在重试... (${i}/${MAX_RETRIES})"
        sleep $RETRY_INTERVAL
        continue
    fi

    STATUS=$(echo "$RESPONSE" | jq -r '.data.status')
    PROGRESS=$(echo "$RESPONSE" | jq -r '.data.progress')

    if [ "$STATUS" = "completed" ]; then
        RESULT=$(echo "$RESPONSE" | jq -r '.data.result')

        SOURCE=$(echo "$RESULT" | jq -r '.source')
        USER_QUESTION=$(echo "$RESULT" | jq -r '.intent_summary.user_question')
        SUMMARY=$(echo "$RESULT" | jq -r '.intent_summary.summary_text')
        STRATEGIES=$(echo "$RESULT" | jq -r '.intent_summary.strategies[]? | "\(.insight)|\(.suggestion)|\(.talking_point)|\(.source_name)|\(.source_date)"' 2>/dev/null || echo "")
        H5_URL=$(echo "$RESULT" | jq -r '.h5_url')

        # 无数据场景
        if [ "$SOURCE" = "none" ]; then
            echo "⚠️ ${SUMMARY}"
            echo ""
            echo "💡 可能的原因："
            echo "  • 公司名称不准确，请确认后重试"
            echo "  • 该公司近期无公开动态"
            echo "  • 该公司为非公开企业，信息较少"
            echo ""
            echo "请确认公司名称是否正确，或提供更多信息以便精准采集。"
            break
        fi

        echo "🔍 ${USER_QUESTION}"
        echo ""
        echo "✅ ${SUMMARY}"
        echo ""

        # 销售策略（只展示最新的2条）
        if [ -n "$STRATEGIES" ]; then
            echo "💡 销售策略："
            echo ""
            echo "$STRATEGIES" | head -n 2 | while IFS= read -r line; do
                [ -n "$line" ] && echo "$line" | awk -F'|' '{
                    printf "🎯 %s\n\n", $1
                    printf "   💼 %s\n\n", $2
                    printf "   💬 \"%s\"\n\n", $3
                    if ($4 != "" || $5 != "") printf "   📡 %s · %s\n\n", $4, $5
                }'
            done
        fi

        echo "📊 [查看完整情报雷达 →](${H5_URL})"

        # 客户检查
        CHECK_RESULT=$(curl -s --max-time 30 "${FASTAPI_BASE_URL}/customer/check?company_name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${COMPANY_NAME}'))")" \
          -H "Authorization: Bearer ${API_TOKEN}" 2>/dev/null)

        if [ $? -eq 0 ] && [ -n "$CHECK_RESULT" ]; then
            EXISTS=$(echo "$CHECK_RESULT" | jq -r '.data.exists')
            if [ "$EXISTS" = "true" ]; then
                # 已添加为客户，不输出任何信息
                :
            else
                echo ""
                echo "💡 该公司未添加为客户，回复"添加"可快速添加"
            fi
        fi

        break
    elif [ "$STATUS" = "failed" ]; then
        ERROR=$(echo "$RESPONSE" | jq -r '.data.error')
        echo "❌ 采集失败：${ERROR}"
        break
    elif [ -n "$PROGRESS" ] && [ "$PROGRESS" != "null" ]; then
        echo "🔍 情报雷达采集中... ${PROGRESS}%"
    fi

    sleep $RETRY_INTERVAL
done

# 轮询超时处理
if [ $i -eq $MAX_RETRIES ]; then
    echo ""
    echo "⏱️ 采集任务超时（已超过20分钟），请稍后通过以下方式查看结果："
    echo "  • 重新发送查询请求"
    echo "  • 或联系管理员检查任务状态"
fi
```

### 轮询接口

```
GET /radar/task/{task_id}
Authorization: Bearer ${API_TOKEN}
```

**响应**：
```json
{
  "code": 0,
  "data": {
    "task_id": "task_xxx",
    "status": "pending|processing|completed|failed",
    "progress": 50,
    "result": {
      "company_id": "szyckj_3f7a",
      "company_name": "数智云创科技有限公司",
      "intent_summary": {
        "intent_type": "query_dynamic",
        "summary_text": "正全力推进数字化转型，近期发布新平台、组建AI团队，是切入技术合作的绝佳时机",
        "strategies": [
          {
            "insight": "新平台上线，带动SaaS与系统集成需求",
            "suggestion": "准备功能分析及相似案例，预约技术总监交流",
            "talking_point": "祝贺贵司新平台上线，在推广中遇到了哪些技术挑战？",
            "source_name": "官网",
            "source_date": "2026-06-07"
          }
        ]
      },
      "h5_url": "http://47.116.49.218:5173/intelligence-radar/szyckj_3f7a?code=xxx"
    }
  }
}
```

---

### 检查客户是否已添加

```
GET /customer/check?company_name={公司名}
Authorization: Bearer ${API_TOKEN}
```

**响应**：
```json
{
  "code": 0,
  "data": {
    "exists": true,
    "customer_id": 123,
    "company_name": "中软国际（中国）科技有限公司"
  }
}
```

---

### 快速添加客户

```
POST /customer/quick-add
Authorization: Bearer ${API_TOKEN}
Content-Type: application/json

{
  "company_name": "中软国际（中国）科技有限公司"
}
```

**响应**：
```json
{
  "code": 0,
  "data": {
    "customer_id": 124,
    "company_name": "中软国际（中国）科技有限公司"
  }
}
```

---

## 换码机制

后端生成换码并返回 H5 链接：

```
H5_URL = "http://47.116.49.218:5173/intelligence-radar/{company_id}?code={exchange_code}"
```

换码由后端管理，包含 `employee_id` 和 `intent_summary`。

---

## 聊天摘要输出

从后端返回的 `intent_summary` 中提取信息输出，**只保留销售最关心的策略**：

```
🔍 {user_question}

✅ {summary_text}

💡 销售策略：
🎯 {insight_1}
   💼 {suggestion_1}
   💬 "{talking_point_1}"
...

📊 [查看完整情报雷达 →]({h5_url})
```

**注意**：
- `user_question` 是用户原始问题
- `summary_text` 由后端 LLM 根据意图动态生成（如"正全力推进HR数字化与AI转型，是切入其技术合作的绝佳时机"），不是固定格式
- 聊天只输出摘要，完整数据（profile、dynamics、strategies 等）通过 H5 链接查看
- SKILL 只负责格式化输出，不参与意图判断和摘要生成

---

## 客户关联检查

### 检查时机
采集完成后（轮询状态为 `completed` 时），自动检查该公司是否已添加为客户。

### 检查逻辑
```bash
# 检查是否已添加为客户
CHECK_RESULT=$(curl -s --max-time 30 "${FASTAPI_BASE_URL}/customer/check?company_name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${COMPANY_NAME}'))")" \
  -H "Authorization: Bearer ${API_TOKEN}" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$CHECK_RESULT" ]; then
    EXISTS=$(echo "$CHECK_RESULT" | jq -r '.data.exists')
    if [ "$EXISTS" = "true" ]; then
        # 已添加为客户，不输出任何信息
        :
    else
        # 未添加为客户，提示用户
        echo ""
        echo "💡 该公司未添加为客户，回复"添加"可快速添加"
        # 保存状态，用于识别用户回复"添加"的意图
        LAST_COMPANY_NAME="${COMPANY_NAME}"
    fi
fi
```

### 用户回复"添加"的处理

**触发条件**：用户输入为"添加"，且上一轮输出过"该公司未添加为客户"提示。

**处理逻辑**：
```bash
# 检查是否是添加客户的回复
if [ "${USER_INPUT}" = "添加" ] && [ -n "${LAST_COMPANY_NAME}" ]; then
    # 调用快速添加客户 API
    ADD_RESULT=$(curl -s --max-time 30 -X POST "${FASTAPI_BASE_URL}/customer/quick-add" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${API_TOKEN}" \
      -d "{\"company_name\": \"${LAST_COMPANY_NAME}\"}" 2>/dev/null)

    if [ $? -eq 0 ] && [ -n "$ADD_RESULT" ]; then
        CUSTOMER_ID=$(echo "$ADD_RESULT" | jq -r '.data.customer_id')
        if [ "$CUSTOMER_ID" != "null" ] && [ -n "$CUSTOMER_ID" ]; then
            echo "✅ 已添加客户 [${LAST_COMPANY_NAME}]"
        else
            ERROR_MSG=$(echo "$ADD_RESULT" | jq -r '.message')
            echo "❌ 添加客户失败：${ERROR_MSG}"
        fi
    else
        echo "❌ 添加客户失败，请稍后重试"
    fi

    # 清除状态
    LAST_COMPANY_NAME=""
fi
```

### 错误处理
- 如果检查客户 API 调用失败（网络错误、超时等），静默处理，不影响主流程输出
- 如果添加客户 API 调用失败，输出错误提示给用户

---

## 重要规则（红线）

1. **🚫 聊天输出红线**：聊天中严禁输出完整的 profile JSON、dynamics 列表、原始采集数据。聊天只允许输出摘要格式。完整数据通过 H5 链接查看。
2. **🚫 系统日志静默**：采集过程中的内部日志（预检结果、API 调用细节、错误处理等）严禁输出给用户。轮询进度提示 `🔍 情报雷达采集中... N%` 为用户友好交互，允许输出。
3. **🚫 绝不编造数据**：未找到的信息标记为"暂无数据"，不猜测不发明。公司名可能不存在时，优先提示用户确认，而非强行采集编造。
4. **时间范围严格 6 个月**：只采集 6 个月内的信息，过期信息不纳入（后端控制）
5. **入库后方可输出**：未成功采集的数据不输出到聊天
6. **不识别意图**：用户原始输入完整传递给后端，不在 SKILL 中做任何意图判断

---

## 使用示例

**示例1：查询动态**
```
用户: "华为最近动态"
→ 提取公司名：华为
→ 输出"🔍 情报雷达正在采集中，请稍候..."
→ [内部] 调用后端采集 → 轮询等待
→ 输出摘要 + H5 链接
→ [内部] 检查客户是否已添加
   → 已添加：不输出
   → 未添加：输出"💡 该公司未添加为客户，回复"添加"可快速添加"
```

**示例2：准备拜访**
```
用户: "我要拜访阿里"
→ 提取公司名：阿里
→ 输出"🔍 情报雷达正在采集中，请稍候..."
→ [内部] 调用后端采集 → 轮询等待
→ 输出摘要 + H5 链接
→ [内部] 检查客户是否已添加
```

**示例3：添加客户**
```
用户: "查询华为"
→ [内部] 完整采集流程
→ 输出摘要 + H5 链接
→ 输出"💡 该公司未添加为客户，回复"添加"可快速添加"

用户: "添加"
→ [内部] 识别为添加客户意图
→ 调用 POST /api/v1/customer/quick-add
→ 输出"✅ 已添加客户 [华为技术有限公司]"
```

**示例4：无数据（公司名错误或信息极少）**
```
用户: "帮我分析华威"（实际想说华为）
→ 提取公司名：华威
→ [内部] 调用后端采集 → LLM 尝试采集 → 无数据
→ 输出"⚠️ 未采集到华威的公开信息"
→ 输出可能原因 + H5 链接
→ 提示用户确认公司名称
```

---

## 自动链式执行

本 Skill 执行完成后，不自动触发其他 Skill。所有分析逻辑已内嵌在后端采集流程中。
