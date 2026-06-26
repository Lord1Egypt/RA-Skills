// ============================================================================
// EO Expert Data - 32 Experts across 8 Major Roles
// ============================================================================
// ---------------------------------------------------------------------------
// 8 Major Roles
// ---------------------------------------------------------------------------
export const ROLES = {
    ARCHITECT: 'architect',
    PLANNER: 'planner',
    FRONTEND: 'frontend',
    BACKEND: 'backend',
    QA: 'qa',
    SECURITY: 'security',
    DEVOPS: 'devops',
    REVIEWER: 'reviewer',
};
// ---------------------------------------------------------------------------
// Expert Registry
// ---------------------------------------------------------------------------
export const EXPERTS = {
    // =========================================================================
    // ARCHITECT (4 experts)
    // =========================================================================
    'arch-001': {
        id: 'arch-001',
        name: 'System Architect',
        role: ROLES.ARCHITECT,
        description: 'Designs large-scale distributed systems with focus on scalability, reliability, and performance.',
        capabilities: ['system-architecture', 'microservices', 'distributed-systems', 'scalability', 'availability'],
        tools: ['draw.io', 'archimate', 'c4-model', 'aws-diagrams'],
        skills: ['architecture', 'tech-selection', 'trade-off-analysis'],
        available: true,
    },
    'arch-002': {
        id: 'arch-002',
        name: 'Frontend Architect',
        role: ROLES.ARCHITECT,
        description: 'Designs frontend architecture including component systems, state management, and performance patterns.',
        capabilities: ['frontend-architecture', 'component-design', 'state-management', 'web-performance', 'ssr-ssg'],
        tools: ['figma', 'storybook', 'webpack-analyzer', 'lighthouse'],
        skills: ['frontend-arch', 'component-design', 'performance-optimization'],
        available: true,
    },
    'arch-003': {
        id: 'arch-003',
        name: 'Data Architect',
        role: ROLES.ARCHITECT,
        description: 'Designs data layer including databases, caching strategies, and data flow architectures.',
        capabilities: ['data-architecture', 'database-design', 'caching-strategy', 'data-modeling', 'etl-design'],
        tools: ['er-studio', 'dbdiagram', 'redis', 'kafka'],
        skills: ['data-model', 'cache-strategy', 'schema-design'],
        available: true,
    },
    'arch-004': {
        id: 'arch-004',
        name: 'Infrastructure Architect',
        role: ROLES.ARCHITECT,
        description: 'Designs cloud infrastructure, networking, and operational architecture for production systems.',
        capabilities: ['infrastructure-design', 'cloud-architecture', 'networking', 'disaster-recovery', 'cost-optimization'],
        tools: ['terraform', 'aws-cdk', 'gcp-deployment-manager', 'arch Diagrams'],
        skills: ['cloud-infra', 'network-design', 'dr-planning'],
        available: true,
    },
    // =========================================================================
    // PLANNER (4 experts)
    // =========================================================================
    'plan-001': {
        id: 'plan-001',
        name: 'Project Planner',
        role: ROLES.PLANNER,
        description: 'Breaks down complex projects into manageable tasks, defines milestones, and creates execution roadmaps.',
        capabilities: ['wbs-creation', 'milestone-planning', 'task-decomposition', 'estimation', 'risk-planning'],
        tools: ['jira', 'ms-project', 'asana', 'monday.com'],
        skills: ['wbs', 'estimation', 'roadmap-planning'],
        available: true,
    },
    'plan-002': {
        id: 'plan-002',
        name: 'Technical Planner',
        role: ROLES.PLANNER,
        description: 'Plans technical implementations with focus on dependencies, technical debt, and delivery sequencing.',
        capabilities: ['technical-planning', 'dependency-analysis', 'sprint-planning', 'release-planning', 'backlog-management'],
        tools: ['jira', 'confluence', 'github-projects', 'linear'],
        skills: ['sprint-planning', 'backlog-grooming', 'release-planning'],
        available: true,
    },
    'plan-003': {
        id: 'plan-003',
        name: 'Product Planner',
        role: ROLES.PLANNER,
        description: 'Translates product requirements into delivery plans with feature prioritization and roadmap alignment.',
        capabilities: ['product-planning', 'feature-prioritization', 'roadmap-alignment', 'requirement-analysis', 'mvp-definition'],
        tools: ['productboard', 'airtable', 'jira', 'roadmunk'],
        skills: ['mvp-planning', 'feature-prioritization', 'requirement-analysis'],
        available: true,
    },
    'plan-004': {
        id: 'plan-004',
        name: 'Scrum Master',
        role: ROLES.PLANNER,
        description: 'Facilitates agile delivery, removes impediments, and coaches teams on agile practices.',
        capabilities: ['sprint-facilitation', 'retrospective-leadership', 'impediment-removal', 'agile-coaching', 'ceremony-facilitation'],
        tools: ['jira', 'confluence', 'scrumwise', 'harvest'],
        skills: ['sprint-management', 'agile-coaching', 'velocity-tracking'],
        available: true,
    },
    // =========================================================================
    // FRONTEND (4 experts)
    // =========================================================================
    'fe-001': {
        id: 'fe-001',
        name: 'React Developer',
        role: ROLES.FRONTEND,
        description: 'Builds React applications with modern patterns including hooks, concurrent features, and performance optimization.',
        capabilities: ['react', 'hooks', 'next.js', 'typescript', 'performance-optimization', 'testing-library'],
        tools: ['vscode', 'react-devtools', 'storybook', 'webpack', 'vite'],
        skills: ['react-development', 'ssr', 'code-splitting'],
        available: true,
    },
    'fe-002': {
        id: 'fe-002',
        name: 'Vue Developer',
        role: ROLES.FRONTEND,
        description: 'Develops Vue.js applications with Composition API, Pinia state management, and Nuxt SSR.',
        capabilities: ['vue', 'nuxt', 'pinia', 'vuex', 'vite', 'typescript'],
        tools: ['vscode', 'vue-devtools', 'storybook', 'vite'],
        skills: ['vue-development', 'ssr', 'state-management'],
        available: true,
    },
    'fe-003': {
        id: 'fe-003',
        name: 'UI/UX Designer',
        role: ROLES.FRONTEND,
        description: 'Creates user interfaces with focus on accessibility, responsive design, and design system implementation.',
        capabilities: ['ui-design', 'design-systems', 'responsive-design', 'accessibility', 'css-architecture'],
        tools: ['figma', 'sketch', 'adobe-xd', 'storybook'],
        skills: ['design-system', 'responsive-css', 'a11y'],
        available: true,
    },
    'fe-004': {
        id: 'fe-004',
        name: 'Mobile Web Developer',
        role: ROLES.FRONTEND,
        description: 'Develops mobile-first web experiences with PWA support, touch optimization, and native-like interactions.',
        capabilities: ['pwa', 'mobile-first', 'touch-optimization', 'service-workers', 'offline-support'],
        tools: ['lighthouse', 'workbox', 'vite', 'chrome-devtools'],
        skills: ['pwa-development', 'touch-ui', 'offline-first'],
        available: true,
    },
    // =========================================================================
    // BACKEND (4 experts)
    // =========================================================================
    'be-001': {
        id: 'be-001',
        name: 'API Developer',
        role: ROLES.BACKEND,
        description: 'Designs and implements RESTful and GraphQL APIs with focus on versioning, documentation, and developer experience.',
        capabilities: ['rest-api', 'graphql', 'openapi', 'api-versioning', 'api-documentation', 'rate-limiting'],
        tools: ['postman', 'swagger', 'stoplight', 'insomnia', 'apifox'],
        skills: ['api-design', 'swagger-docs', 'rate-limiting'],
        available: true,
    },
    'be-002': {
        id: 'be-002',
        name: 'Microservices Developer',
        role: ROLES.BACKEND,
        description: 'Builds microservices architectures with service mesh, event-driven communication, and distributed tracing.',
        capabilities: ['microservices', 'service-mesh', 'event-driven', 'distributed-tracing', 'service-discovery'],
        tools: ['docker', 'kubernetes', 'istio', 'jaeger', 'consul'],
        skills: ['service-design', 'event-sourcing', 'circuit-breaker'],
        available: true,
    },
    'be-003': {
        id: 'be-003',
        name: 'Database Developer',
        role: ROLES.BACKEND,
        description: 'Implements database solutions including SQL optimization, NoSQL patterns, and data migration strategies.',
        capabilities: ['sql', 'postgresql', 'mongodb', 'redis', 'database-optimization', 'data-migration'],
        tools: ['pgadmin', 'mongosh', 'redis-cli', 'dbdiagram', 'liquibase'],
        skills: ['query-optimization', 'schema-design', 'migration'],
        available: true,
    },
    'be-004': {
        id: 'be-004',
        name: 'Authentication Specialist',
        role: ROLES.BACKEND,
        description: 'Implements authentication and authorization systems including OAuth2, JWT, SSO, and identity management.',
        capabilities: ['oauth2', 'jwt', 'sso', 'identity-management', 'mfa', 'password-security'],
        tools: ['keycloak', 'auth0', 'okta', 'firebase-auth', 'ldap'],
        skills: ['auth-implementation', 'token-management', 'session-security'],
        available: true,
    },
    // =========================================================================
    // QA (4 experts)
    // =========================================================================
    'qa-001': {
        id: 'qa-001',
        name: 'Test Engineer',
        role: ROLES.QA,
        description: 'Designs and executes test strategies including functional, integration, and regression testing.',
        capabilities: ['test-planning', 'test-case-design', 'functional-testing', 'integration-testing', 'regression-testing'],
        tools: ['jira', 'testrail', 'zephyr', 'selenium', 'cypress'],
        skills: ['test-design', 'test-execution', 'bug-reporting'],
        available: true,
    },
    'qa-002': {
        id: 'qa-002',
        name: 'Test Automation Engineer',
        role: ROLES.QA,
        description: 'Builds automated test frameworks and CI/CD-integrated test pipelines for continuous quality assurance.',
        capabilities: ['test-automation', 'ci-cd-integration', 'e2e-testing', 'api-testing', 'test-framework-design'],
        tools: ['playwright', 'cypress', 'selenium', 'github-actions', 'jenkins'],
        skills: ['automation-framework', 'e2e-testing', 'pipeline-integration'],
        available: true,
    },
    'qa-003': {
        id: 'qa-003',
        name: 'Performance QA Engineer',
        role: ROLES.QA,
        description: 'Conducts performance testing including load, stress, and scalability testing with detailed profiling.',
        capabilities: ['load-testing', 'stress-testing', 'profiling', 'benchmarking', 'capacity-planning', ' APM'],
        tools: ['jmeter', 'k6', 'gatling', 'new-relic', 'datadog', 'k6-cloud'],
        skills: ['load-profile-design', 'bottleneck-analysis', 'capacity-planning'],
        available: true,
    },
    'qa-004': {
        id: 'qa-004',
        name: 'Security QA Engineer',
        role: ROLES.QA,
        description: 'Performs security testing including OWASP Top 10, penetration testing, and vulnerability assessment.',
        capabilities: ['owasp-testing', 'penetration-testing', 'vulnerability-assessment', 'security-automation', 'secure-code-review'],
        tools: ['owasp-zap', 'burp-suite', 'nmap', 'sqlmap', 'snyk'],
        skills: ['security-testing', 'vuln-assessment', 'secure-test-design'],
        available: true,
    },
    // =========================================================================
    // SECURITY (4 experts)
    // =========================================================================
    'sec-001': {
        id: 'sec-001',
        name: 'Application Security Engineer',
        role: ROLES.SECURITY,
        description: 'Reviews application code for security vulnerabilities, implements secure coding practices, and conducts threat modeling.',
        capabilities: ['secure-code-review', 'threat-modeling', 'sast', 'dast', 'security-architecture'],
        tools: ['sonarqube', 'snyk', 'checkmarx', 'fortify', 'owasp-zap'],
        skills: ['code-security-review', 'threat-modeling', 'secure-design'],
        available: true,
    },
    'sec-002': {
        id: 'sec-002',
        name: 'Infrastructure Security Engineer',
        role: ROLES.SECURITY,
        description: 'Secures cloud and on-premise infrastructure including network security, IAM, and compliance automation.',
        capabilities: ['cloud-security', 'iam', 'network-security', 'compliance', 'infrastructure-hardening'],
        tools: ['aws-security-hub', 'palo-alto', 'vault', 'puppet', 'chef'],
        skills: ['iam-design', 'network-hardening', 'compliance-as-code'],
        available: true,
    },
    'sec-003': {
        id: 'sec-003',
        name: 'DevSecOps Engineer',
        role: ROLES.SECURITY,
        description: 'Integrates security into CI/CD pipelines with automated security scanning, policy enforcement, and incident response.',
        capabilities: ['devsecops', 'security-automation', 'incident-response', 'policy-as-code', 'container-security'],
        tools: ['trivy', 'aqua-security', 'falco', 'pagerduty', 'splunk'],
        skills: ['secure-cicd', 'container-scanning', 'incident-response'],
        available: true,
    },
    'sec-004': {
        id: 'sec-004',
        name: 'Security Auditor',
        role: ROLES.SECURITY,
        description: 'Conducts comprehensive security audits, compliance assessments, and penetration tests against regulatory standards.',
        capabilities: ['security-audit', 'compliance-assessment', 'penetration-testing', 'risk-assessment', 'policy-development'],
        tools: ['nessus', 'qualys', 'metasploit', 'burp-suite', 'gpg'],
        skills: ['audit-execution', 'compliance-checking', 'risk-scoring'],
        available: true,
    },
    // =========================================================================
    // DEVOPS (4 experts)
    // =========================================================================
    'devops-001': {
        id: 'devops-001',
        name: 'CI/CD Engineer',
        role: ROLES.DEVOPS,
        description: 'Designs and implements CI/CD pipelines with automated testing, deployment strategies, and release orchestration.',
        capabilities: ['ci-cd-design', 'pipeline-automation', 'deployment-strategy', 'release-orchestration', 'artifact-management'],
        tools: ['github-actions', 'gitlab-ci', 'jenkins', 'argocd', 'nexus'],
        skills: ['pipeline-design', 'blue-green-deploy', 'canary-release'],
        available: true,
    },
    'devops-002': {
        id: 'devops-002',
        name: 'Kubernetes Engineer',
        role: ROLES.DEVOPS,
        description: 'Operates and optimizes Kubernetes clusters including auto-scaling, resource management, and troubleshooting.',
        capabilities: ['kubernetes', 'container-orchestration', 'helm', 'kustomize', 'auto-scaling', 'cluster-monitoring'],
        tools: ['kubectl', 'helm', 'kustomize', 'prometheus', 'grafana', 'k9s'],
        skills: ['cluster-ops', 'resource-optimization', 'troubleshooting'],
        available: true,
    },
    'devops-003': {
        id: 'devops-003',
        name: 'SRE Engineer',
        role: ROLES.DEVOPS,
        description: 'Implements site reliability practices including SLOs, error budgets, incident management, and postmortem analysis.',
        capabilities: ['slo-definition', 'error-budgets', 'incident-management', 'postmortem', 'reliability-engineering'],
        tools: ['pagerduty', 'opsgenie', 'prometheus', 'grafana', 'runbook'],
        skills: ['slo-design', 'incident-response', 'postmortem'],
        available: true,
    },
    'devops-004': {
        id: 'devops-004',
        name: 'Cloud Infrastructure Engineer',
        role: ROLES.DEVOPS,
        description: 'Manages cloud infrastructure across AWS, GCP, or Azure with infrastructure-as-code and cost optimization.',
        capabilities: ['aws', 'gcp', 'azure', 'infrastructure-as-code', 'cost-optimization', 'multi-cloud'],
        tools: ['terraform', 'pulumi', 'cloudformation', 'terragrunt', 'cost-explorer'],
        skills: ['iac', 'cloud-ops', 'cost-optimization'],
        available: true,
    },
    // =========================================================================
    // REVIEWER (4 experts)
    // =========================================================================
    'rev-001': {
        id: 'rev-001',
        name: 'Code Quality Reviewer',
        role: ROLES.REVIEWER,
        description: 'Reviews code for quality, maintainability, readability, and adherence to coding standards.',
        capabilities: ['code-quality', 'maintainability-review', 'coding-standards', 'refactoring-guidance', 'best-practices'],
        tools: ['sonarqube', 'eslint', 'prettier', 'rubocop', 'gometalinter'],
        skills: ['quality-assessment', 'refactoring-advice', 'standard-enforcement'],
        available: true,
    },
    'rev-002': {
        id: 'rev-002',
        name: 'Security Code Reviewer',
        role: ROLES.REVIEWER,
        description: 'Specializes in identifying security vulnerabilities through manual and automated code review techniques.',
        capabilities: ['security-code-review', 'vulnerability-identification', 'owasp', 'secure-patterns', 'vulnerability-reporting'],
        tools: ['sonarqube', 'snyk', 'semgrep', 'bandit', 'fortify'],
        skills: ['vuln-identification', 'secure-patterns', 'security-reporting'],
        available: true,
    },
    'rev-003': {
        id: 'rev-003',
        name: 'Architecture Reviewer',
        role: ROLES.REVIEWER,
        description: 'Reviews system designs for architectural fitness including scalability, resilience, and technical debt assessment.',
        capabilities: ['architecture-review', 'technical-debt-assessment', 'scalability-review', 'resilience-analysis', 'adr-review'],
        tools: ['draw.io', 'arc42', 'adr-tools', 'architecture-decision Records'],
        skills: ['arch-review', 'debt-assessment', 'resilience-evaluation'],
        available: true,
    },
    'rev-004': {
        id: 'rev-004',
        name: 'Performance Reviewer',
        role: ROLES.REVIEWER,
        description: 'Analyzes code and systems for performance bottlenecks, inefficiency patterns, and optimization opportunities.',
        capabilities: ['performance-analysis', 'bottleneck-identification', 'profiling', 'optimization', 'memory-analysis'],
        tools: ['py-spy', 'async-profiler', 'clinic-js', 'chrome-devtools', 'perf-tools'],
        skills: ['profiling', 'bottleneck-analysis', 'optimization-recommendations'],
        available: true,
    },
};
// ---------------------------------------------------------------------------
// Expert Statistics
// ---------------------------------------------------------------------------
export const EXPERT_STATS = {
    total: Object.keys(EXPERTS).length,
    byRole: (() => {
        const counts = {};
        for (const expert of Object.values(EXPERTS)) {
            counts[expert.role] = (counts[expert.role] ?? 0) + 1;
        }
        return counts;
    })(),
};
// ---------------------------------------------------------------------------
// Role Metadata
// ---------------------------------------------------------------------------
export const ROLE_META = {
    [ROLES.ARCHITECT]: {
        name: 'Architect',
        description: 'System architecture & technology selection',
        icon: '🏗️',
    },
    [ROLES.PLANNER]: {
        name: 'Planner',
        description: 'Project planning, WBS, and roadmap',
        icon: '📋',
    },
    [ROLES.FRONTEND]: {
        name: 'Frontend Developer',
        description: 'UI development, component design',
        icon: '🎨',
    },
    [ROLES.BACKEND]: {
        name: 'Backend Developer',
        description: 'API, services, database layer',
        icon: '⚙️',
    },
    [ROLES.QA]: {
        name: 'QA Engineer',
        description: 'Testing and quality assurance',
        icon: '🧪',
    },
    [ROLES.SECURITY]: {
        name: 'Security Engineer',
        description: 'Security review and hardening',
        icon: '🔒',
    },
    [ROLES.DEVOPS]: {
        name: 'DevOps Engineer',
        description: 'CI/CD, infrastructure, operations',
        icon: '🚀',
    },
    [ROLES.REVIEWER]: {
        name: 'Code Reviewer',
        description: 'Code quality and architecture review',
        icon: '🔍',
    },
};
// ---------------------------------------------------------------------------
// Team Templates
// ---------------------------------------------------------------------------
export const TEAM_TEMPLATES = {
    'fullstack': ['plan-001', 'fe-001', 'be-001', 'qa-001'],
    'web': ['plan-001', 'fe-001', 'be-001', 'qa-001', 'devops-001'],
    'api': ['plan-002', 'be-001', 'be-003', 'qa-002'],
    'data': ['plan-001', 'be-002', 'be-003', 'qa-003'],
    'security': ['sec-001', 'sec-004', 'rev-002'],
    'architecture': ['arch-001', 'arch-003', 'rev-003'],
    'code-review': ['rev-001', 'rev-002'],
    'performance': ['qa-003', 'rev-004', 'devops-003'],
    'deploy': ['devops-001', 'devops-002', 'devops-004', 'devops-003'],
};
//# sourceMappingURL=data.js.map