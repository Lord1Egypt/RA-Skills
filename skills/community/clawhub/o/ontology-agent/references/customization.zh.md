> **中英文双语 — 均可适配**  本文件为中文原版；对应英文版为同名去掉 `.zh` 的文件（如 `customization.md`）。完整中英术语对照见 `references/glossary.yaml`。

# 用户定制机制（私有覆盖，不破坏技能包整体性）

> 核心原则：**技能包提供「武器库」，用户改动只存于自己的私有数据 `company-data/<公司>/instance.yaml`**。
> 无论用户怎么改名、增删部门、指定性别，技能包本体文件一律不动 —— 整体性永远保留，可随时升级同步。

## 一、24 部门库 vs 用户实际团队

- 技能包内置 **24 个部门**（`experts-template/department_experts.yaml`）：12 核心（默认团队）+ 12 可选。
- 用户首次实例化时默认勾选 12 核心；可选部门在引导中按需激活。
- 用户可在「不改技能包」的前提下，对这 24 个做改名、指定性别、停用，或新增完全私有的部门。

## 二、四种私有覆盖（写入 instance.yaml）

| 字段 | 作用 | 是否影响技能包 |
|------|------|----------------|
| `department_aliases: {code: 新名}` | 部门显示名改名（如 `finance` → `财务总监`） | 否，仅本实例 |
| `department_genders: {code: female}` | 指定该部门头像/语感性别 | 否，仅本实例 |
| `disabled_departments: [code]` | 从团队停用某部门 | 否，仅本实例 |
| `custom_departments: [{code,name,gender,expertise,tools_ref,persona}]` | 新增完全私有的 AI 员工 | 否，仅本实例 |

> 优先级：用户私有覆盖 > 技能包部门库默认值。合并逻辑见 `scripts/init.py: resolve_departments()`。

## 三、命令行用法（全存私有数据，零侵入技能包）

```bash
# 列出 24 部门库（看有哪些可选）
python scripts/init.py --catalog

# 列出某公司当前生效的部门
python scripts/init.py --slug weishu --list-depts

# 改名（私有覆盖）
python scripts/init.py --slug weishu --rename finance 财务总监

# 指定性别（仅头像/语感，不影响能力）
python scripts/init.py --slug weishu --gender sales female

# 停用某部门
python scripts/init.py --slug weishu --disable mkt_seo
# 重新启用
python scripts/init.py --slug weishu --enable mkt_seo

# 新增私有部门（完全自定义 AI 员工）
python scripts/init.py --slug weishu --add-dept cso \
    --name 首席安全官 --gender male \
    --expertise "安全战略、合规治理、危机应对" \
    --persona-text "公司安全与合规治理的总负责人，向老板直接汇报"
```

## 四、数字公司的「主动引导」里如何呈现

经营主理人在渐进式引导中，会：
1. 先用完 12 核心（P0 阶段）；
2. 在 P2/P3 阶段**温和提议**若干可选部门（如电商客户可启用 `customer_service`/`csm`），一次只推 1~2 个、可跳过；
3. 明确告诉用户：改名、增删、指定性别都能做，且「**这些改动只在你自己的公司数据里，不会改动技能包本身**」，打消安全顾虑。

## 五、与头像系统的关系

- 每个部门有 `gender_default`（技能包内的合理默认），可被 `department_genders` 覆盖。
- 头像选择逻辑见 `scripts/avatars.py`：按 `(code, gender)` 取技能包头像池；私有部门无专属头像时回退通用池。
- 用户指定性别后，重新生成/同步专家包即可让对应头像生效，技能包本体不变。
