# 验证方法

## 1. 前置验证

```bash
# KooCLI 已安装且版本 ≥ 7.2
hcloud --version

# AK/SK 环境变量已设置且非空
python3 -c "import os; ak=[v for k,v in os.environ.items() if k.upper().startswith('HUAWEI') and ('ACCESS_KEY' in k.upper() or k.upper().endswith('_AK'))]; print('AK:', 'OK' if ak else 'MISSING')"
```

## 2. 认证验证

```bash
# 配置 default profile（脚本自动完成，也可手动）
hcloud configure set --cli-profile=default --cli-access-key=$HUAWEICLOUD_SDK_AK --cli-secret-key=$HUAWEICLOUD_SDK_SK

# 验证配置存在
hcloud configure list
```

## 3. 命令可用性验证

```bash
# CCI 服务操作可列出
hcloud CCI --help | grep -E 'listCoreV1NamespacedPod|readCoreV1NamespacedPod|listNamespaces'

# 某操作的参数说明可获取
hcloud CCI listCoreV1NamespacedPod --help
```

## 4. 真实 API 调用验证

选择一个有 CCI 资源的区域（如 `cn-north-4`）：

```bash
# 列出命名空间（应返回 NamespaceList JSON）
python3 scripts/cci_query.py list-namespaces --region=cn-north-4

# 跨命名空间列出 Pod（无资源时 items 为 null，属正常）
python3 scripts/cci_query.py list-all-pods --region=cn-north-4
```

**判定标准**：

| 输出 | 判定 |
|------|------|
| 返回合法 JSON，含 `kind`/`items` 字段 | ✅ 通过 |
| 返回 `items: []` 或 `items: null` | ✅ 通过（空结果） |
| 返回 `403 CCI.01.403122` | ⚠️ 需 CCI 服务授权（非脚本问题） |
| 返回 `USE_ERROR` / `Traceback` | ❌ 失败 |

## 5. 脚本功能验证

```bash
# --help 正常
python3 scripts/cci_query.py --help

# capability-list 列出全部子命令
python3 scripts/cci_query.py capability-list

# 缺少必填参数时友好报错（退出码 2）
python3 scripts/cci_query.py list-pods --region=cn-north-4
# 应提示 --namespace 必填

# AK/SK 缺失时退出码 3
env -u HUAWEICLOUD_SDK_AK -u HUAWEICLOUD_SDK_SK python3 scripts/cci_query.py list-namespaces --region=cn-north-4
```

## 6. 输出正确性核验

将脚本输出与原生 hcloud 输出对比，应完全一致：

```bash
# 脚本输出
python3 scripts/cci_query.py list-namespaces --region=cn-north-4

# 原生 hcloud 输出
hcloud CCI listNamespaces --cli-region=cn-north-4 --cli-profile=default
```

两者返回的 JSON 内容应一致（脚本只是封装 + 格式化）。
