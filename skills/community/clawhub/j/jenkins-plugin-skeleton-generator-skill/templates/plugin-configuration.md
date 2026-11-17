# 持久化配置模板

```java
package com.example.plugin.config;

import hudson.Extension;
import hudson.model.AbstractDescribableImpl;
import hudson.model.Descriptor;
import org.kohsuke.stapler.DataBoundConstructor;

import java.io.Serializable;

public class PluginConfiguration extends AbstractDescribableImpl<PluginConfiguration> implements Serializable {
    
    private final String key;
    private final String value;

    @DataBoundConstructor
    public PluginConfiguration(String key, String value) {
        this.key = key;
        this.value = value;
    }

    public String getKey() { return key; }
    public String getValue() { return value; }

    @Extension
    public static class DescriptorImpl extends Descriptor<PluginConfiguration> {
        @Override
        public String getDisplayName() {
            return "Plugin Configuration";
        }
    }
}
```
