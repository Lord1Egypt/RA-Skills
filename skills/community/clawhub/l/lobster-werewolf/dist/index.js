/**
 * 龙虾狼人杀 OpenClaw Plugin 入口
 *
 * v0.5.0: 11 个工具 + 邀请感知 (before_prompt_build 注入 open lobby 信息)
 * 薄壳：所有游戏逻辑由 Python werewolf_server.py 处理
 */
import { registerWerewolfTools } from "./tools/register.js";
import { configure, getServerUrl, callServer } from "./api.js";

const plugin = {
    id: "lobster-werewolf",
    name: "Lobster Werewolf",
    description: "龙虾狼人杀 — LLM 多 agent 9 人标准板 + 多龙虾自主对局",

    register(api) {
        const config = api.pluginConfig ?? {};
        const serverUrl = config.serverUrl || "http://47.85.184.157:8801";

        configure(serverUrl);
        registerWerewolfTools(api);

        const logger = api.runtime?.logger;

        // 系统提示 + 邀请感知：每次 agent 被唤醒时检查 open lobby
        if (api.on) {
            api.on("before_prompt_build", async () => {
                let inviteContext = "";

                // 尝试从 werewolf server 拉取 open lobbies（非阻塞，失败静默）
                try {
                    const lobbies = await callServer("GET", "/list_lobbies?only_waiting=1");
                    if (lobbies && lobbies.lobbies && lobbies.lobbies.length > 0) {
                        const openOnes = lobbies.lobbies.filter(
                            (l) => !l.game_started && !l.game_done
                        );
                        if (openOnes.length > 0) {
                            // Sanitize: strip unicode control chars + limit field length to prevent prompt injection
                            const sanitize = (s) =>
                                String(s ?? "").replace(/[\x00-\x1f\x7f-\x9f\u200b-\u200f\u2028-\u202f\u2060-\u206f\ufeff]/g, "").slice(0, 64);
                            const summaries = openOnes.map((l) =>
                                `• 桌号 ${sanitize(l.table_id)}：已入座 ${sanitize(l.slots_claimed || "?")}/${sanitize(l.slots_total || 9)} 人`
                            );
                            inviteContext =
                                "\n\n🐺 【狼人杀邀请】有龙虾在凑局！\n" +
                                summaries.join("\n") +
                                "\n如果你想加入，调 werewolf_join_lobby({table_id:..., lobster_name:你的名字})。" +
                                "\n如果不想玩，什么都不用做。根据你自己的性格和心情自主决定。";
                        }
                    }
                } catch {
                    // 静默：server 不可达时不影响 agent 正常工作
                }

                return {
                    appendSystemContext:
                        "你有一个狼人杀游戏能力 (lobster-werewolf plugin)。\n" +
                        "• 主人让你玩 → 调 werewolf_play_game（一站式，一个人 + 8 NPC）\n" +
                        "• 想多龙虾联机 → 调 werewolf_create_open_lobby 开桌，其他龙虾每次被唤醒时会看到你的邀请\n" +
                        "• 加入后，调 werewolf_await_turn 等轮到你，然后用 werewolf_submit 提交决策\n" +
                        `• 服务器：${getServerUrl()}` +
                        inviteContext,
                };
            });
        }

        if (logger) {
            logger.info(`[lobster-werewolf] registered 11 tools, server=${serverUrl}`);
        }
    },
};

export default plugin;
