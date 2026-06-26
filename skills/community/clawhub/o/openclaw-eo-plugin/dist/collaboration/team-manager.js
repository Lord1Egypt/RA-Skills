// ============================================================================
// EO Team Manager - Expert Team Assembly & Coordination
// ============================================================================
import { getExpert, getExpertTeam } from '../experts/index.js';
// Use crypto.randomUUID if available, fallback
function generateId() {
    try {
        return crypto.randomUUID();
    }
    catch {
        return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
    }
}
// ---------------------------------------------------------------------------
// Team State
// ---------------------------------------------------------------------------
const activeTeams = new Map();
// ---------------------------------------------------------------------------
// Team Manager
// ---------------------------------------------------------------------------
export class TeamManager {
    teams = activeTeams;
    /**
     * Create a new expert team for a task
     */
    createTeam(task, expertIds) {
        const experts = getExpertTeam(expertIds ?? 'default');
        const team = {
            id: generateId(),
            name: `Team-${task.slice(0, 20)}`,
            task,
            experts,
            createdAt: Date.now(),
            status: 'forming',
        };
        this.teams.set(team.id, team);
        return team;
    }
    /**
     * Get a team by ID
     */
    getTeam(teamId) {
        return this.teams.get(teamId);
    }
    /**
     * Update team status
     */
    setTeamStatus(teamId, status) {
        const team = this.teams.get(teamId);
        if (!team)
            return false;
        team.status = status;
        return true;
    }
    /**
     * List all active teams
     */
    listTeams() {
        return Array.from(this.teams.values());
    }
    /**
     * Remove a completed team
     */
    removeTeam(teamId) {
        return this.teams.delete(teamId);
    }
    /**
     * Assemble an expert team with specific roles
     */
    assembleTeam(task, roles) {
        const experts = [];
        for (const role of roles) {
            const expert = getExpert(role);
            if (expert)
                experts.push(expert);
        }
        const team = {
            id: generateId(),
            name: `Team-${task.slice(0, 20)}`,
            task,
            experts,
            createdAt: Date.now(),
            status: 'forming',
        };
        this.teams.set(team.id, team);
        return team;
    }
    /**
     * Get the default team for a task type
     */
    getDefaultTeamForTask(taskType) {
        const taskTeams = {
            'frontend': ['pm', 'frontend-dev', 'qa'],
            'backend': ['pm', 'backend-dev', 'qa'],
            'fullstack': ['pm', 'fullstack-dev', 'qa'],
            'mobile': ['pm', 'mobile-dev', 'qa'],
            'data': ['pm', 'data-engineer', 'dba', 'qa'],
            'ml': ['pm', 'ml-engineer', 'data-engineer', 'qa'],
            'devops': ['devops', 'sre', 'release-manager'],
            'security': ['security-engineer', 'security-auditor'],
            'architecture': ['architect', 'tech-lead', 'dba'],
            'code-review': ['code-reviewer', 'senior-dev'],
            'performance': ['performance-engineer', 'sre'],
        };
        return taskTeams[taskType.toLowerCase()] ?? taskTeams['fullstack'];
    }
}
// Global singleton
export const teamManager = new TeamManager();
//# sourceMappingURL=team-manager.js.map