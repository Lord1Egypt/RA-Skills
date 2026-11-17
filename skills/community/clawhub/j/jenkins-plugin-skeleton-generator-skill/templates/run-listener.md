# RunListener 扩展点模板

```java
package com.example.plugin;

import hudson.Extension;
import hudson.model.Run;
import hudson.model.TaskListener;
import hudson.model.listeners.RunListener;

import javax.annotation.Nonnull;

@Extension
public class YourPluginListener extends RunListener<Run<?, ?>> {

    @Override
    public void onStarted(Run<?, ?> run, TaskListener listener) {
        // 构建开始时触发
        listener.getLogger().println("Build started: " + run.getFullDisplayName());
    }

    @Override
    public void onCompleted(Run<?, ?> run, @Nonnull TaskListener listener) {
        // 构建完成时触发
        listener.getLogger().println("Build completed: " + run.getResult());
    }
}
```
