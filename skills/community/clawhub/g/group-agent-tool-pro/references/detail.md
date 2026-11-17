# 详细参考 - group-agent-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (yaml)

```yaml
deployment:
  mode: enterprise_ha
  nodes: 5
  database:
    backend: postgresql
    cluster: pg-cluster.internal
    ha: true
    replicas: 3

federation:
  enabled: true
  trust_model: tiered

encryption:
  default: tls
  sensitive_groups: e2e
  key_management: vault
  key_rotation: 90d

permissions:
  model: rbac
  roles: [admin, editor, readonly, guest]
  audit: true

integrations:
  - feishu
  - wecom

bots:
  - standup-bot
  - task-bot
  - alert-bot
  - summary-bot

analytics:
  enabled: true
  metrics: [activity, efficiency, contribution]
  report_schedule: monthly

audit:
  enabled: true
  standards: [SOX, 等保2.0]
  retention: 2555  # 7年
  immutable: true

compliance:
  data_residency: cn
  cross_border: restricted
  pii_redaction: required
```

## 代码示例 (python)

```python
from group_agent_pro import GroupBot, bot_registry

@bot_registry.register('task-distributor-bot')
class TaskDistributorBot(GroupBot):
    """自动分发子任务的群机器人"""

    triggers = ['@task-bot', 'task_distribute']

    async def on_mention(self, msg):
        task = self.parse_task(msg.content)

        loads = await self.get_member_loads(msg.group_id)

        assignments = self.assign_task(task, loads)

        for agent, subtask in assignments.items():
            await self.send(
                msg.group_id,
                f"@{agent} 请处理: {subtask.description}",
                mentions=[agent]
            )

    async def on_completion(self, completion_msg):
        result = self.process_result(completion_msg)

        if self.all_complete(completion_msg.task_id):
            await self.send(
                completion_msg.group_id,
                f"任务 {completion_msg.task_id} 全部完成"
            )
```

## 代码示例 (bash)

```bash
group-agent init --mode enterprise \
  --db postgresql://user:pass@db:5432/groups \
  --federation enabled \
  --encryption e2e

group-agent federation register \
  --id instance-hq \
  --endpoint https://agent-hq.company.com

group-agent create \
  --name "跨组织项目协作" \
  --type federation \
  --encryption e2e \
  --audit on

group-agent bot install \
  --group proj-cross-org \
  --bot standup-bot \
  --schedule "0 10 * * *"

group-agent integrate feishu \
  --app-id $FEISHU_APP_ID \
  --app-secret $FEISHU_APP_SECRET
```

## 代码示例 (yaml)

```yaml
federation:
  enabled: true
  instances:
    - id: instance-hq
      endpoint: https://agent-hq.company.com
      trust: full
    - id: instance-bj
      endpoint: https://agent-bj.company.com
      trust: full
    - id: instance-partner
      endpoint: https://partner.external.com
      trust: limited  # 受限信任
  federation_groups:
    - id: cross-org-project
      members:
        - instance-hq:agent_researcher
        - instance-bj:agent_analyst
        - instance-partner:agent_liaison
```

## 代码示例 (yaml)

```yaml
integration:
  - platform: feishu
    mode: bot
    app_id: ${FEISHU_APP_ID}
    app_secret: ${FEISHU_APP_SECRET}
    sync_groups:
      - agent_group: proj-q3
        im_chat: "Q3项目协作群"
      - agent_group: daily-standup
        im_chat: "每日站会群"

  - platform: wecom
    mode: app
    corp_id: ${WECOM_CORP_ID}
    agent_id: ${WECOM_AGENT_ID}
    secret: ${WECOM_SECRET}
```

## 代码示例 (yaml)

```yaml
integration:
  platform: feishu
  mode: bot

  sync_mapping:
    - agent_group: proj-q3
      feishu_chat_id: oc_xxx
      direction: bidirectional
      message_filter:
        - skip_system_messages
        - redact_pii

    - agent_group: daily-standup
      feishu_chat_id: oc_yyy
      direction: agent_to_im  # 仅Agent消息同步至飞书
      schedule: "0 10 * * *"
```

## 代码示例 (yaml)

```yaml
federation:
  trust_model: tiered
  tiers:
    - name: internal
      trust: full
      instances: [instance-hq, instance-bj, instance-sh]
    - name: partner
      trust: limited
      instances: [instance-partner-a, instance-partner-b]
      restrictions:
        - no_sensitive_groups
        - message_redaction_required
    - name: external
      trust: none
      instances: []
```

## 代码示例 (yaml)

```yaml
auth:
  mode: oauth
  provider: azure_ad
  client_id: ${OAUTH_CLIENT_ID}
  client_secret: ${OAUTH_CLIENT_SECRET}
  scopes: [openid, profile, email, groups]

  group_mapping:
    - azure_group: "Agent-Admins"
      role: admin
    - azure_group: "Agent-Editors"
      role: editor
    - azure_group: "Agent-Auditors"
      role: readonly
```

