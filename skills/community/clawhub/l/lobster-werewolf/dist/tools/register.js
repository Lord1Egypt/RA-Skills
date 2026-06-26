/**
 * 注册所有狼人杀工具到 OpenClaw gateway
 */
import {
    werewolfPlayGame,
    werewolfCreateTable,
    werewolfStatus,
    werewolfEvents,
    werewolfHealth,
    werewolfCreateOpenLobby,
    werewolfListLobbies,
    werewolfCreateLobby,
    werewolfJoinLobby,
    werewolfAwaitTurn,
    werewolfSubmit,
} from "./werewolf.js";

export function registerWerewolfTools(api) {
    // v0.1: single-player + NPC (legacy, one-shot)
    api.registerTool(werewolfHealth);
    api.registerTool(werewolfPlayGame);
    api.registerTool(werewolfCreateTable);
    api.registerTool(werewolfStatus);
    api.registerTool(werewolfEvents);

    // v0.5: open lobby (anyone can join)
    api.registerTool(werewolfCreateOpenLobby);

    // v0.3+: multi-lobster lobby with turn-based interactive play
    api.registerTool(werewolfListLobbies);
    api.registerTool(werewolfCreateLobby);
    api.registerTool(werewolfJoinLobby);
    api.registerTool(werewolfAwaitTurn);
    api.registerTool(werewolfSubmit);
}
