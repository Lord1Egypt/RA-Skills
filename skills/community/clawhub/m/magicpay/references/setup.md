# Connection Setup

Install the host-native MagicPay plugin and authenticate the remote MagicPay
MCP that it declares. The plugin contains the skill and host metadata.
No MagicPay package, CLI, library, or local service is installed for the
browser flow.

Any previously installed MagicPay CLI is an abandoned path. Ignore it for
setup, login, verification, and recovery; its presence does not establish a
connection. Do not execute or upgrade it. Use the native plugin and remote MCP.

When authentication is missing, start one browser OAuth flow for both account
verification and MCP authorization. The same connection page collects the email
and OTP, grants MCP access, and redirects to the host. Do not ask the
user to send an email or OTP in chat, and do not run a separate MagicPay account
setup or login flow.

## Plugin lifecycle

Connecting, removing, and revoking MagicPay are host connection-management
actions. Use the host's plugin or connection settings to remove the connection
or revoke its authorization; there is no remote MagicPay removal or revocation
tool. Keep that lifecycle separate from payment orchestration and do not invent
an MCP command for it.

First discover current-conversation MagicPay tools, including deferred tools.
If `get_magicpay_capabilities` is callable, run the readiness sequence below and
verify the requested environment; a missing plugin-inventory action must not
block an already usable connection. An authentication challenge goes to the
host's Connect flow, and a service failure is not proof that installation is
missing. Do not reinstall in response to either error.

When tools are unavailable, inspect the installed plugin and its bundled
connection through the runtime's supported inventory actions. Keep a correct
installation and existing authorization; a repeated setup request is not a
request to update, reinstall, or sign in again. Keep a supported installed
version even when the marketplace advertises a newer release.
Missing tools or an unavailable plugin inventory do not erase a confirmed
installation or completed OAuth. If state has not otherwise been established,
it remains unknown; missing tools do not mean the plugin is absent. Only when
that state is unknown and neither native nor permitted host-command inventory
can be read, use the runtime's plugin-details handoff to establish it. For an
installed plugin, continue through Connect when sign-in is needed; choose
Install/Add only when absence is confirmed. If already connected, discover its
tools and verify readiness. Do not send a correct, loadable plugin back through
Install. If the host reports missing or corrupt installed files, follow only
the runtime reference's documented bundle-repair path; preserve completed sign-in.
Use an actually callable, eligible native installation action, or the
host's supported commands when permitted, as listed in the runtime setup
reference. The agent performs those commands. Do not
automate the host's own settings UI or bypass a denied host action. During an
actual channel change, log out the old exact connection before removing its
plugin; preserve unrelated integrations and all remote account/payment state.

Installation, saved OAuth metadata, accepted authentication, activation in the
current conversation, and readiness are separate. Saved OAuth metadata does
not prove accepted authentication or readiness. Follow the host's activation
result: a cold install may need activation before its Connect action exists.
After authorization has completed, try
current-conversation discovery before requesting a reload. A user-entered reload
or connector attachment is same-conversation recovery, not automatic setup.

## Explain and connect

During routine setup, describe the next user action and the verified result.
Keep environment checks, staging/development references, plugin/catalog IDs,
version numbers, and build revisions out of user-facing narration. Use those
details internally to select and verify the requested connection. Preserve any
exact endpoint required by the host's native confirmation. If setup is blocked,
explain the problem and next action in plain language; include technical
identifiers only when the user explicitly asks for troubleshooting details.

For a first-time setup request, explain the product before opening the
connection UI:

> MagicPay is the broader payment platform redesigned for AI agents. MagicCard
> is MagicPay's omnipayment tool: it has one unified balance, can be topped up
> through supported funding rails, and can pay through supported credit-card,
> crypto, and agentic payment methods. It gives me a secure way to prepare
> payments and request approvals while keeping sensitive payment details out of
> chat.

When you can initiate Connect, set the secure-input boundary:

> I’ll open a secure MagicPay window. Enter your email and OTP there—not in
> this chat. After the host confirms authorization, I’ll verify the connection
> and continue.

Use the runtime's tool-triggered native connection prompt as the primary path
where supported. Calling `get_magicpay_capabilities` can request native OAuth
without a separate Connect tool; discoverable tool definitions do not prove
authentication. A startup authentication failure can prevent any tool result
from reaching that prompt. When tools cannot load, inspect supported host
connection state: an explicit authentication-required result such as
`reauthenticationRequired` follows Connect;
tool absence alone does not justify another login. Keep service and network
failures separate from authentication and activation failures.
Follow the runtime reference before falling back to its supported
connection action. Missing host-management tools do not establish a server outage
or an authentication failure. Never promise an opened window without evidence.

Installing the plugin is not authentication. Inspect the exact installed
`magicpay` connection: check readiness when already authorized, and start Connect
for initial sign-in, an explicit request to open login, or an observed authentication
requirement. When the plugin was just installed for this setup and no completed
sign-in, working authenticated connection, or pending login is known, follow the
runtime's initial sign-in action in this conversation. Cached OAuth metadata alone
must not skip that initial action after confirmed plugin absence; an undetermined
inventory status is not itself a reason to stop or move chats.
Preserve any completed authorization or pending login. Activate a cold installation first when
the host requires it. The install, activation, connect, and recovery actions for
this host are listed in
[references/runtime-setup.md](references/runtime-setup.md), which every runtime
bundle provides for its own host; the canonical instructions never name a host.
Use an actually exposed native Authenticate/Connect action for that existing
connection when authentication is required. Reuse a pending login; do not open
another prompt or send the user to manual settings while it remains active.
The Connect action must open the same secure browser OAuth flow described
above. Never request or handle its email, OTP, authorization code, or tokens in
chat or shell arguments.

Evaluate command eligibility using the runtime reference, current instructions,
and observed host decisions. Missing native controls and historical notes do
not establish a current policy restriction. If a policy blocks the supported
fallback, identify its applicable source or observed denial without exposing
private instructions. Respect actual restrictions; do not invent a session-policy
prohibition or switch routes to bypass a denial.
A restriction limited to agent commands may still permit the documented manual
native handoff; a denied authentication attempt may not be retried by another route.

Do not tell the user that a fresh task or session will open OAuth. Only when
authentication is required and neither a supported native action nor its
permitted command can initiate the connection,
report the blocked phase and give only the immediate manual handoff named in
the runtime setup reference. A manual fallback is not completed single-prompt
setup or proof of an agent-callable authentication control. Host integration
documentation does not make an action callable; do not bridge missing controls
with private RPC, settings UI automation, or a duplicate server.
A canceled or denied action stops this attempt; do not retry through
another route.

Wait for host-reported authorization completion yourself when supported; do not
require a "done" reply. Use a bounded wait or discovery interval and continue
when it succeeds. An opened or closed browser window is not proof of OAuth
completion. Report a cancellation, failure, or deadline at the phase it occurred,
without reopening sign-in automatically.

After OAuth completes, first probe the current task's callable catalog,
including any host-native deferred or lazy tool discovery, for
`get_magicpay_capabilities`. A tool omitted from the initial or eagerly shown
list is not evidence that it is unavailable. If the capability tool is
callable, stay in the current task, run the readiness sequence below, and
continue any request retained there.

If an actual current-task catalog lookup cannot discover or call a required
MagicPay tool, follow the runtime setup reference's bounded supported refresh.
Use a native reload only when it is actually exposed to the model; otherwise
follow the runtime reference's documented activation recovery, which may use
a fresh conversation after confirmed installation and authorization. Keep its
recovery cue and reuse the installation and sign-in. Do not repeat an already
attempted recovery step; use a further step only when its documented evidence
requirements are met, otherwise report the observed host limit. Missing tools alone do
not diagnose stale state, failed authentication, or a particular host limitation.
Use activation recovery only when no separate authentication or service error
is observed. An explicit authentication requirement follows Connect even if a
previous login succeeded; a new conversation does not complete authentication.
Keep installation, host-reported authorization, tool availability, and service
readiness separate: report only the phases supported by evidence. Do not repeat
OAuth for missing tools alone, install a MagicPay CLI, start a local MCP server,
copy a token, or claim that a refreshed task retained an unfinished request from
the old task.

Call `get_magicpay_capabilities`. Continue only when it reports
`executionModes: ["client_browser"]`, `sessionAuthority: "remote_database"`, and
`browserPaymentRun.executionMode: "agent_direct"`. Treat its `setupState`, `nextAction`, and
`instructions` as the authoritative setup continuation. Authentication recovery
belongs to the host's MCP connection UI; the protected server cannot truthfully
return a pre-authentication account state before the host completes OAuth.

Before a fresh payment in a newly connected task, require the rail-specific
capability: `x402PaymentRun.status: "ready"` for x402,
`cryptoPaymentRun.status: "ready"` for crypto, or
`browserPaymentRun.status: "ready"` with `executionMode: "agent_direct"` before
browser payment. The
x402 and crypto workflow contract is `magicpay.payment-run/v1` schema `1.1`;
the browser contract is `magicpay.browser-payment/v1` schema `1.0`.
Use each rail's advertised `minimumPluginVersion` as its compatibility floor;
compare the installed base semantic version without a prerelease suffix. Do not
replace that floor with the newest published version. Verify the exact endpoint
and environment for the selected channel. Guide, plugin, and MCP revisions are
diagnostics; independently deployed services do not need matching Git SHAs.
Preserve the selected rail's `selectedAgentId`. A blocked result is a pre-payment
stop; do not create a session or fall back to another browser-payment tool.

After capability discovery succeeds, call `get_magicpay_status` to verify the
authenticated agent identity and account health. Treat a bounded unavailable
status as an authentication or service-recovery stop; do not infer readiness
from capability discovery alone.

When capabilities and authenticated status are ready, silently call
`get_payment_balance` without an asset selector. Do not call
`show_payment_balance`, a retired card-balance tool, or any presentation tool
for this setup read. Use the response's exact atomic `available` value,
`presentation.scale`, and `presentation.assetId`; the tool's human-readable
content is produced by the shared money formatter. Never use floating point or
invent a currency.

For an explicit setup request, present exactly one of these completion
branches:

- **Funded balance.** If all three payment rails are ready, say:

  > **MagicPay is ready.**
  >
  > Your available balance is **{formatted balance}**.
  >
  > Your payment credentials stay protected and out of chat, and spending
  > stays subject to your MagicPay approval rules.
  >
  > Give it a try—send USDT or USDC, pay with x402, or ask me to buy something
  > online.

  If only some rails are ready, keep the first three paragraphs unchanged and
  offer only the actions whose rail-specific capabilities report `ready`.
- **Exact zero balance.** Keep the same heading, exact formatted balance, and
  credential/approval reassurance, then say: "Add funds to start using
  MagicPay, or ask me to top up your MagicCard." Do not create a top-up link or
  open a widget unless the user asks or the authoritative workflow returns
  `funding_required`.
- **Unavailable or malformed balance.** Say: "**MagicPay is ready.** I couldn't
  read your available balance right now. Your payment credentials stay
  protected and out of chat, and spending stays subject to your MagicPay
  approval rules." Do not infer zero, manufacture an amount or currency, or
  claim that the balance call succeeded.

Then continue the user's original request without asking them to repeat it only
when the host retained that request in this same task. In a catalog-refresh
fallback, act only on the request available after refresh without claiming that
prior task context carried over. In later already-connected tasks, do not repeat
setup onboarding; verify only the capabilities required by the requested action.
Reauthentication is not payment approval. For an interrupted payment, read and
continue the exact existing operation through its returned recovery path,
preserving required approval; do not start a duplicate run or replacement purchase.
