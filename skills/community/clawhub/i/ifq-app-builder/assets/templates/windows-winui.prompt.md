---
templateId: T-windows-winui
ifqMode: A-03
stack: "WinUI 3 + .NET 8 + C#"
artifact: "MSIX / .exe installer"
---

# T-windows-winui · native Windows · ifq-app-builder

Fork this file as `<slug>.prompt.md`, fill every `<replace: ...>`, run `npm run verify:lite -- <slug>.prompt.md`, hand to the coding agent.

## S1 — WHO + WHAT
<replace: who uses this Windows app, what they do every day, what data goes in and out>

## S2 — WHERE
- Platform: Windows 10 build 19041+, Windows 11 (x64 + ARM64)
- Stack (pinned): WinUI 3 (Windows App SDK 1.5+), .NET 8, C# 12, MVVM via CommunityToolkit.Mvvm
- Runtime: 100% local; no telemetry; explicit network scope per feature
- Distribution: <replace: MSIX via Microsoft Store · or signed .exe via private download · or Intune/SCCM enterprise>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful first run on a fresh Windows 11 box>

## Acceptance (binary, yes/no observable)
- [ ] `dotnet run` opens a window under 2s on a Windows 11 laptop
- [ ] Primary workflow from S1 succeeds with <replace: real sample input>
- [ ] Light + dark theme both render correctly; Mica or Acrylic backdrop respected
- [ ] All strings localized via `.resw` files (`zh-CN` + `en-US`)
- [ ] No `System.Exception` thrown during the happy path; logs written to `%LOCALAPPDATA%\<Slug>\logs\`
- [ ] `msbuild /p:Configuration=Release` produces a self-contained MSIX

## Scaffold (run order)
1. `dotnet --version` — confirm 8.0+
2. `dotnet new winui -n <Slug>` (requires `Microsoft.WindowsAppSDK.ProjectTemplates`)
3. Add `CommunityToolkit.Mvvm` and `CommunityToolkit.WinUI` NuGet packages
4. Create `IFQTheme.xaml` ResourceDictionary with the IFQ tokens
5. Implement the workflow per S1; keep file/network I/O in `Services/` and inject via the built-in MVVM DI
6. Add `Strings/zh-CN/Resources.resw` and `Strings/en-US/Resources.resw`
7. `msbuild /restore /p:Platform=x64 /p:Configuration=Release /p:GenerateAppxPackageOnBuild=true`

## Packaging
- MSIX: signed with a code-sign cert; output `<Slug>_<version>_x64.msix`
- `.exe`: optional `Inno Setup` or `Velopack` for a classic installer (only if user explicitly wants it)
- ARM64: separate target if user is on Surface / Snapdragon X devices

## Security baseline (OWASP-aligned)
- Package identity declared; required capabilities minimal in `Package.appxmanifest`
- DPAPI (`ProtectedData`) for any local secret; never plain `app.config`
- Validate every file path against `Path.GetFullPath` + an allowlist root
- No `Process.Start(userInput)`

## IFQ ambient
- `IFQTheme.xaml`: brushes/font sources mapped to `assets/ifq-brand/ifq-tokens.css` values
- About flyout: a single `<TextBlock>— shaped with ifq.ai/app-builder</TextBlock>`

## Agent execution contract
- Print the three sentences back before scaffolding
- If `dotnet 8` is missing, stop and label `S3.packaging` as `(blocked: install .NET 8 SDK)`
- Never trust user input in path joins; use `Path.Combine` + canonical-root check

— shaped with ifq.ai/app-builder · A-03 · T-windows-winui
