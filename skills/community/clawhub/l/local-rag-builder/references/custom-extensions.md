# 自定义扩展（插件注册） — local-rag-builder

本技能支持通过代码注册自定义切分策略和守卫。注册后自动出现在 Web UI 的下拉列表中，配置表单自动生成。

```python
from text_splitter import register_strategy, register_guard, StrategyPlugin, GuardPlugin, Guard

# 自定义切分策略
def my_splitter(text, my_param=100, **kwargs):
    from langchain_core.documents import Document
    # 自定义切分逻辑
    return [Document(page_content=text)]

register_strategy(StrategyPlugin(
    "my_split", "我的自定义切分", my_splitter,
    config_schema={
        "my_param": {"type": "int", "label": "参数名", "default": 100, "min": 1, "max": 1000},
        "flag": {"type": "bool", "label": "开关", "default": False},
    },
    default_config={"my_param": 100, "flag": False},
))

# 自定义守卫
my_guard = Guard("my_guard", re.compile(r'```special\n[\s\S]*?\n```'))
register_guard(GuardPlugin("my_guard", "保护特殊代码块", my_guard))
```
