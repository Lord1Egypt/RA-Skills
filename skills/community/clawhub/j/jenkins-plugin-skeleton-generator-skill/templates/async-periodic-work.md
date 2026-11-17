# 异步任务模板（AsyncPeriodicWork）

```java
import hudson.Extension;
import hudson.model.AsyncPeriodicWork;
import hudson.model.TaskListener;

@Extension
public class YourAsyncPlugin extends AsyncPeriodicWork {

    public YourAsyncPlugin() {
        super("Your Plugin Async Task");
    }

    @Override
    protected void execute(TaskListener listener) throws Exception {
        // 异步执行逻辑
        listener.getLogger().println("Async task executed at: " + System.currentTimeMillis());
    }

    @Override
    public long getRecurrencePeriod() {
        return MIN * 5; // 每5分钟执行一次
    }
}
```
