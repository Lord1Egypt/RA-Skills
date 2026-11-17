# Builder 扩展点模板

```java
package com.example.plugin;

import hudson.Extension;
import hudson.Launcher;
import hudson.model.AbstractProject;
import hudson.model.Run;
import hudson.model.TaskListener;
import hudson.tasks.BuildStepDescriptor;
import hudson.tasks.Builder;
import jenkins.tasks.SimpleBuildStep;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.stapler.DataBoundSetter;

import javax.annotation.Nonnull;
import java.io.Serializable;

public class YourPluginBuilder extends Builder implements SimpleBuildStep, Serializable {

    private final String message;
    private boolean useTimestamp;

    @DataBoundConstructor
    public YourPluginBuilder(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    @DataBoundSetter
    public void setUseTimestamp(boolean useTimestamp) {
        this.useTimestamp = useTimestamp;
    }

    public boolean isUseTimestamp() {
        return useTimestamp;
    }

    @Override
    public void perform(@Nonnull Run<?, ?> run, @Nonnull FilePath workspace, 
                        @Nonnull Launcher launcher, @Nonnull TaskListener listener) 
                        throws InterruptedException, IOException {
        // 构建逻辑 - 在构建执行阶段触发
        listener.getLogger().println("Executing plugin: " + message);
        if (useTimestamp) {
            listener.getLogger().println("Timestamp: " + System.currentTimeMillis());
        }
    }

    @Extension
    public static final class DescriptorImpl extends BuildStepDescriptor<Builder> {

        @Override
        public boolean isApplicable(Class<? extends AbstractProject> jobType) {
            return true;
        }

        @Override
        @Nonnull
        public String getDisplayName() {
            return "用户提供的插件名称";
        }
    }
}
```
