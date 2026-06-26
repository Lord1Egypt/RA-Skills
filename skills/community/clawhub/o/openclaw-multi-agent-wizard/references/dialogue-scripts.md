# Dialogue Scripts

Use these scripts as tone and pacing guides. Do not copy them rigidly when the user's situation is clearly different, but stay close to this level of simplicity.

## Opening script

Good opening:

- "I’ll help you set up OpenClaw multi-agent step by step. You do not need to understand the technical details. I’ll first check whether your OpenClaw is ready."

Bad opening:

- "We need to configure agents, bindings, account routing, peer IDs, and Feishu app permissions."

## Preflight result script

If things look healthy:

- "Your OpenClaw looks ready. We can continue."

If the gateway is down:

- "Your gateway is not running yet. I’ll start it first, then we’ll continue."

If the user already has setup:

- "You already have some OpenClaw settings. I’ll avoid overwriting them and only add the new pieces."

## Mode recommendation script

Use a life-like question:

- "Do you want each robot to have its own assistant, or do you want one robot to act differently in different Feishu groups?"

If recommending `多 bot 多 agent`:

- "I recommend the first option for beginners. It is the easiest to understand and the hardest to break."

If the user says they do not know which mode to choose:

- "If you're not sure, start with one robot for one assistant. That is the safest beginner setup."

If recommending `单 bot 多 agent`:

- "We can use one robot and split by Feishu group. That keeps the entry point simple."

## Mode explanation script

For `多 bot 多 agent`:

- "This means one robot uses one assistant. For example, your work robot uses the work assistant, and your life robot uses the life assistant."

For `单 bot 多 agent`:

- "This means one robot is shared, but different Feishu groups use different assistants. For example, the product group uses the product assistant, and the engineering group uses the engineering assistant."

For advanced mode:

- "This is the version where one assistant can call other assistants to help in the middle of a task. It is powerful, but it is not the best starting point."

If the user insists on agent collaboration:

- "The safest way to do that in Feishu is to let one main assistant reply in the group, while the other assistants help in the background."

## Agent creation script

When creating a new agent:

- "I’ll create the agent for you and also write its basic role files, so it won’t start as an empty shell."

If the user asks what those files are:

- "I’ll prepare a small starter set for this agent, including its identity, role, memory, tools, and user-facing focus. You don’t need to write these by hand."

## Feishu handoff script

When switching from OpenClaw to Feishu platform steps:

- "Next I’ll guide you through the Feishu side. I’ll give you one small step at a time."

When asking for credentials:

- "Please copy the `App ID` and `App Secret` from Feishu and paste them here. After that, I’ll handle the OpenClaw side."

If the user says they cannot find the credentials:

- "Look for the basic app information page in Feishu. If you can see the app overview or app credentials area, the `App ID` and `App Secret` should be there."

For `多 bot 多 agent`, if there will be multiple bots:

- "We’ll set up one Feishu bot first, make sure it works, and then repeat the same steps for the next bot."

When moving to the second bot:

- "The second bot uses the same Feishu steps as the first one. We’ll just repeat the same path, so this part should be faster now."

## Group routing script

For single-bot setup:

- "Now add the bot to the target Feishu group and send one message there. I’ll use that message to identify the group for you."

If the user wants many groups at once:

- "To keep this simple, let’s finish one group first. After that, we can add the second group the same way."

Do not say:

- "Please locate the group chat_id manually."

## Success script

- "Setup complete. I’ll now summarize what was created and tell you the exact message to send for your first test."

## Failure script

When something fails:

- "The setup changes are saved, but I still need to check one thing before calling this done."

Then give exactly one next action.

If the user sounds lost inside Feishu:

- "Tell me the page title or the menu items you can see in Feishu, and I’ll point you to the next click."
