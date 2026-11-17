# Jelly 表单控件参考

生成 Jenkins 插件配置界面时使用的 Jelly 控件。该文档也作为 SKILL 生成 config.jelly 时的参考。

## 基础控件

### `<f:textbox>` — 文本输入框

```xml
<f:entry title="消息内容" field="message">
    <f:textbox default="Hello Jenkins"/>
</f:entry>
```

### `<f:checkbox>` — 复选框

```xml
<f:entry title="启用调试模式" field="debugMode">
    <f:checkbox default="false"/>
</f:entry>
```

### `<f:password>` — 密码输入框

```xml
<f:entry title="API Token" field="apiToken">
    <f:password/>
</f:entry>
```

### `<f:textarea>` — 多行文本域

```xml
<f:entry title="脚本内容" field="scriptContent">
    <f:textarea default=""/>
</f:entry>
```

### `<f:number>` — 数字输入

```xml
<f:entry title="超时时间（秒）" field="timeout">
    <f:number default="30"/>
</f:entry>
```

---

## 选择控件

### `<f:dropdownList>`（JENKINS-59062 后）— 下拉选择

```xml
<f:entry title="日志级别" field="logLevel">
    <f:dropdownList default="INFO"/>
</f:entry>
```

> 注意：需在 Descriptor 中实现 `doFillLogLevelItems()` 方法返回下拉选项。

### `<f:select>` — 传统下拉选择

```xml
<f:entry title="通知方式" field="notifyMethod">
    <select name="notifyMethod">
        <option value="email">邮件</option>
        <option value="webhook">Webhook</option>
        <option value="log">仅日志</option>
    </select>
</f:entry>
```

### `<f:radioBlock>` — 单选按钮组

```xml
<f:entry title="输出格式" field="format">
    <f:radioBlock name="format" value="plain" title="纯文本" checked="true">
        <f:entry title="分隔符" field="separator">
            <f:textbox default=" - "/>
        </f:entry>
    </f:radioBlock>
    <f:radioBlock name="format" value="json" title="JSON">
        <f:entry title="缩进" field="indent">
            <f:checkbox default="true"/>
        </f:entry>
    </f:radioBlock>
</f:entry>
```

---

## 高级控件

### `<f:repeatable>` — 可重复列表

```xml
<f:entry title="自定义参数">
    <f:repeatable field="parameters" minimum="1" header="参数">
        <f:entry title="键" field="key">
            <f:textbox/>
        </f:entry>
        <f:entry title="值" field="value">
            <f:textbox/>
        </f:entry>
        <f:entry title="">
            <div align="right">
                <f:repeatableDeleteButton/>
            </div>
        </f:entry>
    </f:repeatable>
</f:entry>
```

### `<f:hetero-list>` — 异构列表（多类型配置）

```xml
<f:entry title="通知列表">
    <f:hetero-list name="notifications"
                   hasHeader="true"
                   descriptors="${descriptor.notificationDescriptors}"
                   items="${instance.notifications}"
                   addCaption="添加通知"/>
</f:entry>
```

---

## 常见布局模式

### 复选框 + 条件展开

```xml
<f:entry title="启用高级选项" field="useAdvanced">
    <f:checkbox/>
</f:entry>
<f:optionalBlock name="useAdvanced" title="高级选项" checked="${instance.useAdvanced}">
    <f:entry title="重试次数" field="retryCount">
        <f:number default="3"/>
    </f:entry>
</f:optionalBlock>
```

### 带验证的输入

```xml
<f:entry title="端口号" field="port">
    <f:number clazz="positive-number" default="8080"/>
</f:entry>
```

### 文件路径选择器

```xml
<f:entry title="配置文件路径" field="configPath">
    <f:textbox/>
</f:entry>
```

---

## 字段命名对照

Jelly 中 `field` 属性值必须与 Java 类中的 getter/setter 名称对应：

| Java 字段 | Getter | Setter | Jelly field |
|-----------|--------|--------|-------------|
| `private String name;` | `getName()` | `setName()` | `name` |
| `private boolean enabled;` | `isEnabled()` | `setEnabled()` | `enabled` |
| `private int maxRetries;` | `getMaxRetries()` | `setMaxRetries()` | `maxRetries` |
