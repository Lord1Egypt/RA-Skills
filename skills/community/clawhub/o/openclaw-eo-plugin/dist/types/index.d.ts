/**
 * EO Plugin - Type Definitions
 */
export interface Expert {
    id: string;
    name: string;
    role: string;
    description: string;
    /** Capabilities/specializations of this expert */
    capabilities?: string[];
    /** Tools this expert uses */
    tools?: string[];
    /** System prompt for subagent invocation */
    prompt?: string;
    /** Expert-specific skills */
    skills?: string[];
    available?: boolean;
}
export interface Team {
    id: string;
    name: string;
    members: Expert[];
    status: 'planning' | 'active' | 'completed';
    createdAt: Date;
}
export interface ProjectPlan {
    id: string;
    name: string;
    milestones: Milestone[];
    team: Team;
    status: 'draft' | 'approved' | 'in_progress' | 'completed';
}
export interface Milestone {
    id: string;
    name: string;
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    tasks: string[];
    completion: number;
}
export interface ArchitectureDesign {
    id: string;
    projectName: string;
    techStack: TechChoice[];
    modules: Module[];
    risks: Risk[];
    status: 'draft' | 'approved' | 'rejected';
}
export interface TechChoice {
    layer: string;
    technology: string;
    version: string;
    reason: string;
}
export interface Module {
    name: string;
    responsibility: string;
    api: string;
    dependencies: string[];
}
export interface Risk {
    name: string;
    impact: 'low' | 'medium' | 'high';
    probability: 'low' | 'medium' | 'high';
    mitigation: string;
}
export interface CheckpointResult {
    checkpoint: string;
    passed: boolean;
    items: CheckItem[];
    summary: {
        total: number;
        passed: number;
        warnings: number;
        failed: number;
    };
}
export interface CheckItem {
    id: string;
    name: string;
    status: 'pass' | 'fail' | 'warn' | 'skip';
    message?: string;
    details?: string[];
}
export type TeamStatus = 'forming' | 'active' | 'completed' | 'failed';
export interface ExpertTeam {
    id: string;
    name: string;
    task: string;
    experts: Expert[];
    createdAt: number;
    status: TeamStatus;
}
export interface ExpertResult {
    expertId: string;
    expertName: string;
    output: string;
    durationMs: number;
    success: boolean;
    error?: string;
}
export interface CollaborationSession {
    id: string;
    task: string;
    context: Record<string, unknown>;
    teams: ExpertTeam[];
    results: ExpertResult[];
    status: 'running' | 'completed' | 'failed';
    createdAt: number;
    completedAt?: number;
}
export interface PlanOptions {
    task: string;
    team?: string[];
    constraints?: string[];
    priority?: 'low' | 'medium' | 'high';
    context?: Record<string, unknown>;
}
export interface ArchitectOptions {
    task: string;
    style?: string;
    language?: string;
    context?: Record<string, unknown>;
}
export interface VerifyOptions {
    target: string;
    type: 'code' | 'architecture' | 'test' | 'security' | 'performance' | 'accessibility';
    criteria?: string[];
    context?: Record<string, unknown>;
}
export interface CodeReviewOptions {
    files?: string[];
    prUrl?: string;
    focus?: string[];
    depth?: 'quick' | 'standard' | 'deep';
}
export interface EOCommandResult {
    success: boolean;
    command: string;
    output: string;
    expertResults?: ExpertResult[];
    durationMs: number;
    error?: string;
}
export interface EOSkill {
    name: string;
    description: string;
    trigger: string | string[];
    experts: string[];
    steps?: SkillStep[];
    output?: string;
}
export interface SkillStep {
    step: number;
    expert: string;
    input: string;
    output: string;
    verify?: string;
    timeoutMs?: number;
}
export interface PluginCommandContext {
    args?: string;
    userId?: string;
    channel?: string;
    workspace?: string;
    sessionId?: string;
}
export interface PluginCommandResult {
    text: string;
    success?: boolean;
    error?: string;
}
//# sourceMappingURL=index.d.ts.map