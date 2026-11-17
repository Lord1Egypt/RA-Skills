# 数据流图

## 1. 端到端数据流

```text
┌────────────┐   参数（region/alias/key-id/state/limit/输出模式）
│  Agent /   │──────────────────────────────────────────────┐
│    用户    │                                              ▼
└────────────┘                              ┌───────────────────────────┐
                                            │ scripts/list_kms_keys.py  │
                                            │ 1. 只读守卫（写意图 → rc=1）│
                                            │ 2. 参数校验（limit/state） │
                                            └─────────────┬─────────────┘
                                                          │
                              ┌───────────────────────────┴────────────────┐
                              ▼                                            ▼
                   ┌─────────────────────┐                  ┌────────────────────────┐
                   │ 主路径：KooCLI       │   缺失/失败       │ 回退：huaweicloudsdk    │
                   │ hcloud KMS ListKeys │─────────────────▶│ KmsClient.list_keys()  │
                   │ --key_spec=ALL      │   （403/凭据错误  │ 凭据：环境变量 AK/SK     │
                   │ --limit --marker    │    不回退，直接报）│                        │
                   └──────────┬──────────┘                  └───────────┬────────────┘
                              │                                         │
                              └───────────────┬─────────────────────────┘
                                              ▼
                              ┌──────────────────────────────────┐
                              │ KMS OpenAPI                      │
                              │ POST /v1.0/{project_id}/kms/     │
                              │        list-keys                 │
                              └───────────────┬──────────────────┘
                                              ▼
                       {keys[], key_details[], total, truncated, next_marker}
                                              │
                          ┌───────────────────┴────────────────────┐
                          ▼                                        ▼
              truncated=true 且 next_marker 非空        最后一页 / 无 marker
                          │                                        │
                          └── 带上 --marker 再取一页 ◀──────────────┘
                                              │
                                              ▼
                                  ┌───────────────────────┐
                                  │ 归一化 + 客户端过滤     │
                                  │ alias/key_id/state    │
                                  └───────────┬───────────┘
                                              ▼
                     ┌────────────────┬───────────────┬────────────────┐
                     ▼                ▼               ▼                ▼
              默认紧凑列表       --table 8 列      --json 原始体   空列表提示
           （别名/ID/状态）    （含轮转周期）     （合并后响应）    rc=0
                                              │
                                              ▼ （可选，仅 --table）
                              ┌──────────────────────────────────┐
                              │ ShowKeyRotationStatus（逐 key）   │
                              │ POST .../get-key-rotation-status │
                              │ → rotation_interval（30~365 天）   │
                              └──────────────────────────────────┘
```

## 2. 分页数据流

```text
page1: --limit=100                 → truncated=true,  next_marker="m1"
page2: --limit=100 --marker=m1     → truncated=true,  next_marker="m2"
page3: --limit=100 --marker=m2     → truncated=false, next_marker=""
合并：keys[] 与 key_details[] 按 key_id 去重，total 取响应值
安全阀：--max-pages（默认 50）防止异常响应导致死循环
```

## 3. 只读边界

```text
允许的操作集合 = { ListKeys, ShowKeyRotationStatus }
写意图检测顺序：
  --action 非 list            → rc=1（不发起任何调用）
  --alias/--key-id 含写 token  → rc=1（不发起任何调用）
  → 通过后才进入后端调用
```

## 4. 凭据与密钥材料流向

```text
AK/SK ──▶ KooCLI profile / 环境变量 ──▶ hcloud 进程内使用
                                       （脚本不读取、不回显、不落盘）
AK/SK ──▶ HUAWEICLOUD_SDK_AK/SK ──▶ BasicCredentials（仅 SDK 回退路径）

密钥材料（key material）──────────────── 本 skill 从不请求、从不输出
```