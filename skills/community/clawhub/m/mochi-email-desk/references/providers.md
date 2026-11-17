# Provider setup

Copy samples/profile.example.json to a user-private location, set incoming and smtp from your provider, then set the named environment variable privately. Use the FULL mailbox address as username. Enable the relevant protocols in the mailbox settings. Chinese providers commonly use a generated client authorization code; use that instead of the web login password. For all providers, a mailbox administrator may restrict client access.

## Mainland China

- QQ/Foxmail: IMAP imap.qq.com:993 SSL, SMTP smtp.qq.com:465 SSL. Enable service and generate an authorization code in QQ Mail account settings. [QQ Mail support](https://service.mail.qq.com/).
- NetEase 163 / 126 / yeah.net: select the IMAP and SMTP hosts displayed in that mailbox's POP3/SMTP/IMAP settings (commonly imap.163.com / smtp.163.com, imap.126.com / smtp.126.com, imap.yeah.net / smtp.yeah.net), SSL 993 / 465. Use its authorization code; the IMAP adapter sends client ID when advertised. [NetEase help](https://help.mail.163.com/).
- Aliyun personal: imap.aliyun.com:993 / smtp.aliyun.com:465 SSL. [Official ports](https://help.aliyun.com/zh/document_detail/465307.html).
- Alibaba enterprise: imap.qiye.aliyun.com:993 / smtp.qiye.aliyun.com:465 SSL. [Official ports](https://help.aliyun.com/zh/document_detail/36576.html).
- Tencent enterprise, 139, 189, Sina and custom domains: use the client configuration from the mailbox's official account settings. Set explicit hosts/ports and SSL/STARTTLS in the same profile; do not infer an enterprise server from its email suffix.

## International

- Gmail/Google Workspace: imap.gmail.com:993 SSL; smtp.gmail.com:465 SSL or 587 STARTTLS. Use XOAUTH2 or an available app password. OAuth full-mail scope https://mail.google.com/ and app consent are configured in your own Google project. [Protocol setup](https://developers.google.com/workspace/gmail/imap/imap-smtp), [XOAUTH2](https://developers.google.com/workspace/gmail/imap/xoauth2-protocol).
- Outlook.com / Microsoft 365: outlook.office365.com:993 SSL; smtp-mail.outlook.com:587 STARTTLS for personal Outlook, smtp.office365.com:587 STARTTLS for M365. Use OAuth2 and your own Entra client ID. Scopes are IMAP.AccessAsUser.All / SMTP.Send as documented; tenant SMTP AUTH policy must allow the connection. [Microsoft authentication](https://learn.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth), [Outlook ports](https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings-for-outlook-com-d088b986-291d-42b8-9564-9c414e2aa040).
- iCloud: imap.mail.me.com:993 SSL; smtp.mail.me.com:587 STARTTLS, full mailbox address and an app-specific password. IMAP only. [Apple setup](https://support.apple.com/102525).
- Yahoo: imap.mail.yahoo.com:993 SSL; smtp.mail.yahoo.com:465 SSL or 587 STARTTLS, generated app password. [Yahoo setup](https://help.yahoo.com/kb/SLN4075.html).
- Zoho: choose the regional hosts shown in your account; personal US examples imap.zoho.com:993 and smtp.zoho.com:465. Organization plans/regions may use imappro/smtppro or regional domains. [Zoho setup](https://www.zoho.com/mail/help/imap-access.html).
- Fastmail: imap.fastmail.com:993 SSL; smtp.fastmail.com:465 SSL or 587 STARTTLS, app password and a plan with mail-client access. [Fastmail setup](https://www.fastmail.help/hc/en-us/articles/1500000278342-Server-names-and-ports).
- Proton Mail uses its local Bridge, not a direct public IMAP endpoint. This version requires trusted SSL/STARTTLS; use a properly trusted Bridge certificate or the provider's own client. Do not disable certificate checks.

## OAuth profile

Set auth to oauth2. Either reference accessTokenEnv, refreshed by your credential manager, or oauth:{provider:google|microsoft,clientId,refreshTokenEnv,rotatedTokenFile}. Microsoft tenant defaults to common; clientSecretEnv/scope are optional provider-app settings. The initial interactive authorization is performed with the provider's official flow. Put rotatedTokenFile in a private directory outside the Skill installation. Refresh tokens and client secrets never belong in command arguments or chat. A refresh response with a rotated token is retained there for the next call.

Compatibility is implemented at protocol level. Package tests use controlled IMAP/POP3/SMTP fixtures, not authenticated accounts at every provider. After configuration, sync one mailbox, search a known subject, send a test to your own address and confirm receipt. POP3 offers UIDL downloads and local searches, not folders/flags. Current search covers cached mail. Network restrictions and cloud SMTP egress rules must permit the selected mail servers.
