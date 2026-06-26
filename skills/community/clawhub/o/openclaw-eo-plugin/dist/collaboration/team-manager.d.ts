import type { ExpertTeam, TeamStatus } from '../types/index.js';
export declare class TeamManager {
    private teams;
    /**
     * Create a new expert team for a task
     */
    createTeam(task: string, expertIds?: string | string[]): ExpertTeam;
    /**
     * Get a team by ID
     */
    getTeam(teamId: string): ExpertTeam | undefined;
    /**
     * Update team status
     */
    setTeamStatus(teamId: string, status: TeamStatus): boolean;
    /**
     * List all active teams
     */
    listTeams(): ExpertTeam[];
    /**
     * Remove a completed team
     */
    removeTeam(teamId: string): boolean;
    /**
     * Assemble an expert team with specific roles
     */
    assembleTeam(task: string, roles: string[]): ExpertTeam;
    /**
     * Get the default team for a task type
     */
    getDefaultTeamForTask(taskType: string): string[];
}
export declare const teamManager: TeamManager;
//# sourceMappingURL=team-manager.d.ts.map