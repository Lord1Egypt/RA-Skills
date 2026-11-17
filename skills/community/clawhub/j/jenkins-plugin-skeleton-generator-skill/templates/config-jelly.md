# Jelly 配置界面模板

## 基础模板

以下是一个 Builder / Publisher 类型插件的基础配置界面模板：

```xml
<?jelly escape-by-default='true'?>
<j:jelly xmlns:j="jelly:core" xmlns:f="/lib/form">
    <f:entry title="消息" field="message">
        <f:textbox default="Hello Jenkins"/>
    </f:entry>
    <f:entry title="包含时间戳" field="useTimestamp">
        <f:checkbox default="false"/>
    </f:entry>
</j:jelly>
```

## 扩展模板

根据用户配置项类型，可组合使用以下控件。生成 config.jelly 时，每个 Java 字段对应一个 `<f:entry>` 块：

| Java 字段类型 | 推荐 Jelly 控件 | 代码片段 |
|--------------|----------------|---------|
| `String` | `<f:textbox/>` | `<f:entry title="名称" field="name"><f:textbox default="默认值"/></f:entry>` |
| `boolean` | `<f:checkbox/>` | `<f:entry title="是否启用" field="enabled"><f:checkbox default="false"/></f:entry>` |
| `int` | `<f:number/>` | `<f:entry title="数量" field="count"><f:number default="1"/></f:entry>` |
| `String`（多行） | `<f:textarea/>` | `<f:entry title="内容" field="content"><f:textarea default=""/></f:entry>` |
| `String`（密钥） | `<f:password/>` | `<f:entry title="Token" field="token"><f:password/></f:entry>` |
| 枚举选择 | `<select>` | `<f:entry title="级别" field="level"><select name="level">...</select></f:entry>` |

> 所有 Jelly 控件类型和用法详见 `references/jelly-reference.md`
