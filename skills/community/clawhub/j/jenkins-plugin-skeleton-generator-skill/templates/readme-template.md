# 项目 README 模板

```markdown
# {{PLUGIN_DISPLAY_NAME}}
<!-- 示例: "构建审计插件" -->

{{PLUGIN_DESCRIPTION}}
<!-- 示例: "记录每次构建的关键信息到日志，支持自定义日志级别和输出格式" -->

## 特性

- 基于 Jenkins {{JENKINS_VERSION}} 开发
<!-- 示例: "2.426" -->
- 扩展点类型：{{EXTENSION_TYPE}}
<!-- 示例: "RunListener" -->
- 触发时机：{{TRIGGER_TIMING}}
<!-- 示例: "构建开始和完成时自动触发" -->
{{FEATURE_LIST}}
<!-- 根据用户选择动态生成，示例:
  - 异步执行：每 5 分钟清理一次过期日志（用户选择异步时）
  - 持久化配置：支持自定义日志级别和输出目录（用户选择持久化时）
  - 全局配置：在 Manage Jenkins 中统一配置默认参数（用户选择全局配置时）
-->

## 环境要求

| 组件 | 最低版本 |
|------|---------|
| Jenkins | {{JENKINS_VERSION}} |
| JDK | {{JDK_VERSION}} |
| Maven | {{MAVEN_VERSION}} |
<!-- 示例: 3.6+ -->

## 安装

### 通过 Jenkins 插件管理中心

1. 下载 `{{ARTIFACT_ID}}.hpi`
   <!-- 示例: "build-auditor.hpi" -->
2. 登录 Jenkins，进入 **Manage Jenkins** → **Plugins** → **Advanced**
3. 在 **Upload Plugin** 区域上传 `.hpi` 文件
4. 重启 Jenkins

### 手动安装

```bash
cp {{ARTIFACT_ID}}.hpi $JENKINS_HOME/plugins/
# 重启 Jenkins
```

## 使用方式

### {{USAGE_TITLE}}
<!-- 根据插件类型生成对应标题，示例:
  Builder:     "在项目中使用"
  Publisher:   "配置构建后操作"
  RunListener: "自动监听"
  Trigger:     "设置定时触发"
-->

{{USAGE_DESCRIPTION}}
<!-- 根据插件类型生成说明文字，示例 (Builder):
  "1. 打开任意 Jenkins 项目的配置页面
   2. 在「构建」区域点击「增加构建步骤」
   3. 选择「{{PLUGIN_DISPLAY_NAME}}」
   4. 填写配置参数后保存
   5. 触发构建即可看到插件输出"
-->

## 配置说明

{{CONFIGURATION_DETAILS}}
<!-- 如果无持久化配置则省略此段；有则填入说明，示例:
  "所有配置项均保存在 Jenkins 全局配置中，重启不会丢失。"
-->

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
{{CONFIG_ITEMS}}
<!-- 根据 Java 类的字段生成，每个字段一行，示例:
  | message | 字符串 | "Hello Jenkins" | 构建时输出的消息内容 |
  | useTimestamp | 布尔 | false | 是否在消息后追加时间戳 |
  | logLevel | 下拉选择 | "INFO" | 日志输出级别：DEBUG / INFO / WARN / ERROR |
-->

## 开发

### 构建

```bash
# 清理并打包
mvn clean package

# 本地测试运行
mvn hpi:run

# 跳过测试打包
mvn clean package -DskipTests
```

输出产物：`target/{{ARTIFACT_ID}}.hpi`

### 项目结构

```
{{ARTIFACT_ID}}/
├── pom.xml
├── README.md
├── .gitignore
├── src/
│   ├── main/
│   │   ├── java/{{PACKAGE_PATH}}/
│   │   │   ├── {{MAIN_CLASS}}.java
│   │   │   ├── {{MAIN_CLASS}}Descriptor.java
│   │   │   └── config/
│   │   ├── resources/
│   │   │   └── {{PACKAGE_PATH}}/{{MAIN_CLASS}}/
│   │   │       ├── config.jelly
│   │   │       └── help.html
│   │   └── webapp/
│   └── test/
│       └── java/{{PACKAGE_PATH}}/
│           └── {{MAIN_CLASS}}Test.java
```

## 兼容性

| Jenkins 版本 | 状态 |
|--------------|------|
| {{JENKINS_VERSION}}+ | 支持 |

## 许可

{{LICENSE_INFO}}
<!-- 示例: "MIT License" -->
```
