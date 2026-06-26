# `/cursor` Command Patterns

Use these chat commands when the plugin is installed:

```text
/cursor doctor
/cursor list
/cursor status myproj-auth-20260318-180000
/cursor send myproj-auth-20260318-180000 /status
/cursor send myproj-auth-20260318-180000 把 JWT 改成 RS256
/cursor kill myproj-auth-20260318-180000 --force
/cursor spawn feature-auth || 实现 JWT 登录接口 || /mnt/d/project/myapp
```

## Recommendations

- Prefer tools over chat commands when the caller is another agent or workflow.
- Prefer `/cursor doctor` before the first production use.
- In Windows + WSL mode, `projectPath` should use the Linux path form such as `/mnt/d/project/...`.
