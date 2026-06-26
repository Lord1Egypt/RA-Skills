#!/bin/bash
# 群消息超时监控 - 本地计算脚本
#
# 输入：从标准输入接收筛选后的记录 JSON（feishu_bitable_app_table_record list 返回的 records 数组）
# 输出：超过30分钟未回复的记录，按所在群分组
#
# 依赖：jq
#
# usage: cat records.json | bash /workspace/群消息检查/scripts/check.sh

set -euo pipefail

# 当前时间戳（北京时间，单位：秒）
now=$(TZ=Asia/Shanghai date +%s)

# 读取输入
input=$(cat)

if [ -z "$input" ] || [ "$input" = "[]" ]; then
  echo '[]'
  exit 0
fi

# 逐条计算超时，筛选 >30分钟，然后按群分组
echo "$input" | jq -c --argjson now "$now" '
  # 第一步：筛选 >30分钟
  [.[] | select(
    (.["发送时间"] | length) > 0 and
    ((($now - (.["发送时间"] / 1000)) / 60) > 30)
  )]

  # 如果结果为空，直接返回空数组
  | if length == 0 then []
    else
      # 第二步：按所在群的 id 分组
      group_by(.["所在群"][0].id)

      # 第三步：重组为分组格式
      | map({
          chat_id:  .[0]["所在群"][0].id,
          chat_name: .[0]["所在群"][0].name,
          records: [.[] | {
            record_id: .record_id,
            message_id: (.["消息ID"][0].text // ""),
            send_time_ms: .["发送时间"],
            link: (.["消息链接"] // ""),
            content: (.["聊天记录"][0].text // ""),
            chat_name: .["所在群"][0].name
          }]
        })
      | map(select(.records | length > 0))
    end
'
