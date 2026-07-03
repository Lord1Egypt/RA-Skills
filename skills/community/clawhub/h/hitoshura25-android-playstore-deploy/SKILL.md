---
name: Android应用商店部署工具
description: 一个帮助开发者设置自动化Google Play商店部署流程的工具，支持项目分析、密钥生成、服务账户配置和GitHub Actions工作流生成。
version: 1.0.0
---

# Android应用商店部署工具

一个帮助开发者设置自动化Google Play商店部署流程的工具，支持项目分析、密钥生成、服务账户配置和GitHub Actions工作流生成。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Analyze an Android project to understand its configuration and identify requirements for Play Store deployment


Args:

    project_path: Absolute path to the Android project root directory



Returns:
    Result from analyze_android_project
 | `scripts.tools.analyze_android_project` |
| Generate a new Android keystore file for app signing with secure parameters


Args:

    output_path: Absolute path where the keystore will be saved

    alias: Key alias for the signing key

    key_password: Password for the signing key

    store_password: Password for the keystore

    validity_days: How many days the key should be valid

    key_size: Key size in bits

    dname: Distinguished name for the certificate



Returns:
    Result from generate_keystore
 | `scripts.tools.generate_keystore` |
| Generate Gradle signing configuration with dual-source support

Generates signing configuration that works seamlessly for both local development and CI/CD:
- Environment variables (prioritized for CI/CD)
- gradle.properties fallback (for local development)
- Task-based validation (debug builds always work)

Automatically generates gradle.properties.template for easy local setup.

Args:

    project_path: Path to Android project

    env_var_prefix: Prefix for environment variables (default: "APP_")
                   Example: "APP_" creates APP_SIGNING_KEY_STORE_PATH
                   Use "" for no prefix


Returns:
    Result including gradle_config_kotlin, gradle_properties_template, and setup instructions
 | `scripts.tools.generate_signing_config` |
| Provide interactive step-by-step guide for setting up Google Play Service Account


Returns:
    Result from setup_service_account_guide
 | `scripts.tools.setup_service_account_guide` |
| Generate a complete GitHub Actions workflow file for Play Store deployment


Args:

    project_path: Path to Android project

    package_name: Android app package name

    track: Play Store release track (internal, alpha, beta, production)

    trigger_strategy: How to trigger the workflow (manual, branch, tag)

    branch_name: Branch name to trigger on if trigger_strategy is branch

    app_module_path: Path to app module relative to project root

    java_version: Java/JDK version to use for builds

    enforce_proguard: If True, ensure isMinifyEnabled=true in build.gradle.kts (default: True)

    mapping_file_path: Override default ProGuard mapping file path

    include_release_notes: Include release notes directory (default: True)

    release_notes_directory: Path to release notes directory (default: distribution/whatsnew)

    env_var_prefix: Prefix for environment variables (default: "APP_")
                   Example: "APP_" creates APP_SIGNING_KEY_STORE_PATH
                   Use "" for no prefix



Returns:
    Result from generate_github_workflow
 | `scripts.tools.generate_github_workflow` |
| Validate that required GitHub Secrets are configured (checks existence only)


Args:

    repo_owner: GitHub repository owner username or organization

    repo_name: GitHub repository name

    github_token: GitHub Personal Access Token with repo scope

    required_secrets: List of secret names to check for



Returns:
    Result from validate_github_secrets
 | `scripts.tools.validate_github_secrets` |
| Generate a comprehensive guide for creating all required GitHub Secrets


Args:

    repo_url: GitHub repository URL

    keystore_path: Optional path to keystore for encoding instructions



Returns:
    Result from create_github_secrets_guide
 | `scripts.tools.create_github_secrets_guide` |
| Validate that Play Store app and API access are properly configured using service account


Args:

    service_account_json_path: Path to service account JSON file

    package_name: Android app package name to validate



Returns:
    Result from validate_play_store_setup
 | `scripts.tools.validate_play_store_setup` |
| Test the deployment workflow locally without uploading to Play Store


Args:

    project_path: Path to Android project

    keystore_path: Path to keystore file

    store_password: Keystore password

    key_alias: Key alias

    key_password: Key password

    dry_run: If true, skip actual Play Store upload



Returns:
    Result from test_deployment_workflow
 | `scripts.tools.test_deployment_workflow` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.analyze_android_project
工具描述：Analyze an Android project to understand its configuration and identify requirements for Play Store deployment


Args:

    project_path: Absolute path to the Android project root directory



Returns:
    Result from analyze_android_project

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|project_path|string|true| |null|

---

## scripts.tools.generate_keystore
工具描述：Generate a new Android keystore file for app signing with secure parameters


Args:

    output_path: Absolute path where the keystore will be saved

    alias: Key alias for the signing key

    key_password: Password for the signing key

    store_password: Password for the keystore

    validity_days: How many days the key should be valid

    key_size: Key size in bits

    dname: Distinguished name for the certificate



Returns:
    Result from generate_keystore

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|output_path|string|true| |null|
|alias|string|true| |null|
|key_password|string|true| |null|
|store_password|string|true| |null|
|validity_days|integer|false| |null|
|key_size|integer|false| |null|
|dname|string|false| |null|

---

## scripts.tools.generate_signing_config
工具描述：Generate Gradle signing configuration with dual-source support

Generates signing configuration that works seamlessly for both local development and CI/CD:
- Environment variables (prioritized for CI/CD)
- gradle.properties fallback (for local development)
- Task-based validation (debug builds always work)

Automatically generates gradle.properties.template for easy local setup.

Args:

    project_path: Path to Android project

    env_var_prefix: Prefix for environment variables (default: "APP_")
                   Example: "APP_" creates APP_SIGNING_KEY_STORE_PATH
                   Use "" for no prefix


Returns:
    Result including gradle_config_kotlin, gradle_properties_template, and setup instructions

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|project_path|string|true| |null|
|env_var_prefix|string|false|"APP_"|null|

---

## scripts.tools.setup_service_account_guide
工具描述：Provide interactive step-by-step guide for setting up Google Play Service Account


Returns:
    Result from setup_service_account_guide

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.generate_github_workflow
工具描述：Generate a complete GitHub Actions workflow file for Play Store deployment


Args:

    project_path: Path to Android project

    package_name: Android app package name

    track: Play Store release track (internal, alpha, beta, production)

    trigger_strategy: How to trigger the workflow (manual, branch, tag)

    branch_name: Branch name to trigger on if trigger_strategy is branch

    app_module_path: Path to app module relative to project root

    java_version: Java/JDK version to use for builds

    enforce_proguard: If True, ensure isMinifyEnabled=true in build.gradle.kts (default: True)

    mapping_file_path: Override default ProGuard mapping file path

    include_release_notes: Include release notes directory (default: True)

    release_notes_directory: Path to release notes directory (default: distribution/whatsnew)

    env_var_prefix: Prefix for environment variables (default: "APP_")
                   Example: "APP_" creates APP_SIGNING_KEY_STORE_PATH
                   Use "" for no prefix



Returns:
    Result from generate_github_workflow

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|project_path|string|true| |null|
|package_name|string|true| |null|
|track|string|false| |null|
|trigger_strategy|string|false| |null|
|branch_name|string|false| |null|
|app_module_path|string|false| |null|
|java_version|string|false| |null|
|enforce_proguard|boolean|false|true|null|
|mapping_file_path|string|false| |null|
|include_release_notes|boolean|false|true|null|
|release_notes_directory|string|false| |null|
|env_var_prefix|string|false|"APP_"|null|

---

## scripts.tools.validate_github_secrets
工具描述：Validate that required GitHub Secrets are configured (checks existence only)


Args:

    repo_owner: GitHub repository owner username or organization

    repo_name: GitHub repository name

    github_token: GitHub Personal Access Token with repo scope

    required_secrets: List of secret names to check for



Returns:
    Result from validate_github_secrets

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|repo_owner|string|true| |null|
|repo_name|string|true| |null|
|github_token|string|true| |null|
|required_secrets|string|false| |null|

---

## scripts.tools.create_github_secrets_guide
工具描述：Generate a comprehensive guide for creating all required GitHub Secrets


Args:

    repo_url: GitHub repository URL

    keystore_path: Optional path to keystore for encoding instructions



Returns:
    Result from create_github_secrets_guide

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|repo_url|string|true| |null|
|keystore_path|string|false| |null|

---

## scripts.tools.validate_play_store_setup
工具描述：Validate that Play Store app and API access are properly configured using service account


Args:

    service_account_json_path: Path to service account JSON file

    package_name: Android app package name to validate



Returns:
    Result from validate_play_store_setup

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|service_account_json_path|string|true| |null|
|package_name|string|true| |null|

---

## scripts.tools.test_deployment_workflow
工具描述：Test the deployment workflow locally without uploading to Play Store


Args:

    project_path: Path to Android project

    keystore_path: Path to keystore file

    store_password: Keystore password

    key_alias: Key alias

    key_password: Key password

    dry_run: If true, skip actual Play Store upload



Returns:
    Result from test_deployment_workflow

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|project_path|string|true| |null|
|keystore_path|string|true| |null|
|store_password|string|true| |null|
|key_alias|string|true| |null|
|key_password|string|true| |null|
|dry_run|boolean|false| |null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据