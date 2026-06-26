export class SessionContextCache {
    currentContext = null;
    lastUpdate = 0;
    isBrainChecked = false;
    TTL = 60000; // 1 minute TTL
    async ensureContext(projectManager) {
        const now = Date.now();
        // Return cached if still valid
        if (this.currentContext && (now - this.lastUpdate) < this.TTL) {
            return this.currentContext;
        }
        // Auto-load fresh context
        try {
            const project = projectManager.getCurrentProject();
            if (!project)
                return null;
            const overview = await projectManager.searchContext('Project Overview', 3);
            this.currentContext = overview;
            this.lastUpdate = now;
            console.error(`[SessionCache] Auto-loaded context for: ${project}`);
            return overview;
        }
        catch (err) {
            console.error(`[SessionCache] Failed to load context:`, err);
            return null;
        }
    }
    setBrainChecked(checked) {
        this.isBrainChecked = checked;
    }
    hasBeenBrainChecked() {
        return this.isBrainChecked;
    }
    getContext() {
        return this.currentContext;
    }
    invalidate() {
        this.currentContext = null;
        this.lastUpdate = 0;
        this.isBrainChecked = false;
    }
}
