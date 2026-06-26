import { MuninClient } from "@kalera/munin-sdk";
export function createOpenClawMuninAdapter(config) {
    const client = new MuninClient(config);
    return {
        execute: (projectId, action, payload) => client.invoke(projectId, action, payload, { ensureCapability: true }),
        capabilities: () => client.capabilities(),
    };
}
