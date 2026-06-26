# v1.23.0 — 默认权限模型反转 + 附件硬规则

发布日期: 2026-05-07

## 一句话

`odoo_connect` 默认从「全员共享」反转为「按 sender_id 隔离」,让 Odoo 内部 RBAC 真正起作用;同时给 LLM 加附件硬规则,杜绝「解压看到内容跟商机字段对不上就打回用户」的越权行为。

---

## 触发本次发版的事故

用户在企微群里上传 `AI报价单.rar` 让 LLM 建商机。LLM 解压后回复:

> 等等,我解压出来的这批文件内容是工厂生产排产计划,和 Odoo19 商机的内容对不上。你发的可能不是同一个压缩包?

用户被迫解释一通。然后说要让 LLM 帮建商机:

> 应该是每个同事都需要输入自己的账号密码。为了就是不同人拥有不同的权限

但 v1.22 prompt 主动建议「配一次咱们组织所有同事就都能用了 👍」——直接跟用户期望相反。

两件事暴露了:

1. **权限模型设计错误**:v1.10 起默认 `scope='shared'` 让所有人共用同一个 Odoo 账号 → Odoo 内部 RBAC 完全失效(销售/管理员看到的数据一样)
2. **LLM 越权解读附件内容**:插件没有 prompt 级硬约束,LLM 看到附件内容跟"商机"字面对不上就替用户做"内容相符性"判断

---

## Bug 1: 默认凭据 scope 反转

### 旧行为(v1.10–v1.22)

```ts
// config-manager.ts
saveOdooConfig(odooConfig, agentId, scope: 'shared' | 'agent' = 'shared')

// odoo_connect tool
private?: boolean   // false=shared(默认), true=agent
const scope = params.private ? 'agent' : 'shared';
```

prompt 主动建议:

> 配一次之后,所有同事 @ 我都能用,不需要再输入

后果:

- 一个销售配了自己账号 → 全员都用销售账号 → 销售看不到管理员看的数据? 或者更糟:**所有人都看到销售看的数据**(包括财务 / HR / 客户隐私)
- Odoo 用户 RBAC 完全失效。设计得很精细的 group_ids / record_rule 形同虚设
- 不符合企业协作模型("每人按角色分权限"是绝大多数企业期望)

### 新行为(v1.23)

```ts
// config-manager.ts
saveOdooConfig(odooConfig, agentId, scope: 'shared' | 'agent' = 'agent')

// odoo_connect tool —— 新增 shared 参数,语义反转,旧 private 标 deprecated 但仍兼容
{
  shared?: boolean,   // 默认 false = sender_id 隔离 = per-user RBAC
  private?: boolean,  // [deprecated] 仍兼容旧 agent memory:private=true → agent
}

// 优先级:shared 显式 > private 兼容 > 默认 agent
let scope: 'shared' | 'agent';
if (typeof params.shared === 'boolean') scope = params.shared ? 'shared' : 'agent';
else if (typeof params.private === 'boolean') scope = params.private ? 'agent' : 'shared';
else scope = 'agent';
```

prompt 改成:

> 每个同事用自己的账号,权限按你的 Odoo 角色区分(销售看销售的、管理员看管理员的)。绝不要主动建议「配一次全员通用」。

### Fallback 链不变

```
{agentId}.json    ← 默认写这里(per-sender_id)
default.json      ← shared=true 时写这里,作为兜底 fallback
pluginConfig.odoo ← manifest 静态预填(老路径)
odoo-config.json  ← legacy
```

如果用户真的有"组织共用一个公共只读账号"场景,显式说"组织共用",LLM 会调 `odoo_connect(shared=true)` 写 default.json。

---

## Bug 2: 附件硬规则

### 旧行为

prompt 没有任何关于"附件内容判断"的约束。LLM 看到附件,自然按"读了就要用"的常识做内容相符性判断,看到不一致就打回用户。

### 新行为

`before_prompt_build` hook 注入硬规则(未连接 + 已连接两段都加):

> **附件 / 文件内容判断 — 硬规则**
>
> 1. 附件内容由用户负责。不要解读"内容是不是跟商机字段对得上"
> 2. 解压/读附件**仅用于提取用户明示的字段**
> 3. **正确工作流**:`odoo_crm_create` 建商机 → `odoo_attach_file` 挂附件 → 回报完成
> 4. 用户没说要看附件内容时**绝不主动解析后质疑**用户
> 5. 只有用户**明确问**"这附件是什么"时才解读
>
> 常见错误回复:「我解压出来的内容跟商机对不上,你发错了吗?」 ❌

理论依据:`feedback_tool_description_vs_prompt_level_constraint.md` —— 把具体 anti-pattern 字面写进 prompt,比抽象描述有效得多。直接把用户截屏里 LLM 那句越权回复抄进 prompt 当反例,LLM 下次就不会复制粘贴自己的烂回复。

---

## Breaking changes

`odoo_connect` 默认 scope 反转。**已有 v1.22 部署的影响**:

- 已存在的 `default.json`(shared 凭据) **不会被自动迁移或删除**,fallback 链照常工作 → 没有显式 sender_id 配置的成员仍走 shared。
- 已有 `{agentId}.json` 也照常生效(优先级最高)。
- **首次升级后用户主动调 `odoo_connect`**:写入位置变了(从 default.json → {agentId}.json)。如果用户希望继续共享,必须显式说"组织共用"或传 shared=true。

**迁移建议**:升级到 v1.23 后,各成员各自 @ 机器人调一次 `odoo_connect` 配自己账号即可。已存在的 default.json 留作兜底,不影响。

---

## 文件变化

- `src/modules/config-manager.ts` — `saveOdooConfig` 默认参数 `'shared'` → `'agent'`,文件头注释改写说明权限模型反转
- `index.ts`
  - `odoo_connect` schema 加 `shared` 参数,`private` 标 deprecated 但仍兼容
  - `odoo_connect` description 强化:**绝不主动建议全员共用**
  - handler 加 shared > private > 默认 agent 的优先级判断
  - `odoo_whoami` 兜底文案改写
  - `before_prompt_build` hook 未连接段:文案翻新 + 加附件硬规则
  - `before_prompt_build` hook 已连接段:credSourceLabel 改写 + 加附件硬规则
- `SKILL.md` — 首次配置段、Changelog、附件硬规则段
- `package.json` / `openclaw.plugin.json` — 版本 bump 到 1.23.0,description 同步

---

## 自查 checklist

- [x] `compat.pluginApi` 是 ranged(`>=2026.2.24`)
- [x] `package.json.version` / `openclaw.plugin.json.version` / `SKILL.md.version` 三处一致 = 1.23.0
- [x] 没引入 `child_process` / `execSync` / `spawnSync`
- [x] typecheck 通过
- [x] `odoo_connect` 旧 `private` 参数仍兼容(避免老 agent memory 里的调用失败)
- [x] SKILL.md 大小 < 25KB

---

## 关联

- 触发事件: 2026-05-07 用户企微群 LLM 越权回复 + 默认全员共享反馈
- 上游 memory: `feedback_plugins_must_be_independently_installable.md` / `feedback_tool_description_vs_prompt_level_constraint.md`
- 下游 memory: 本次会沉淀 `feedback_default_permission_model_per_user_vs_shared.md`(详见会话末尾)
