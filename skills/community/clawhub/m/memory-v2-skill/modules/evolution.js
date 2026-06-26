/**
 * Evolution Module
 * Track skill proficiency and growth
 */

class EvolutionModule {
    constructor(db) {
        this.db = db;
        this.levelNames = {
            1: 'Novice',
            2: 'Beginner',
            3: 'Intermediate',
            4: 'Advanced',
            5: 'Expert',
            6: 'Master'
        };
        
        this.levelThresholds = {
            1: 0,
            2: 100,
            3: 300,
            4: 600,
            5: 1000,
            6: 1500
        };
    }

    /**
     * Record skill usage
     */
    async recordUsage(skillName, skillCategory, result = 'success', metrics = {}) {
        // Check if skill exists
        let skill = await this.db.get(
            'SELECT * FROM memory_evolution WHERE skill_name = ?',
            [skillName]
        );

        if (!skill) {
            // Create new skill record
            const result = await this.db.run(
                `INSERT INTO memory_evolution (skill_name, skill_category, first_used_at)
                 VALUES (?, ?, CURRENT_TIMESTAMP)`,
                [skillName, skillCategory]
            );
            skill = { id: result.id, proficiency_level: 1, experience_points: 0 };
        }

        // Calculate XP gain
        const xpGain = this.calculateXP(result, metrics);
        const newXP = skill.experience_points + xpGain;
        const newLevel = this.calculateLevel(newXP);
        const oldLevel = skill.proficiency_level;

        // Update skill record
        await this.db.run(
            `UPDATE memory_evolution 
             SET usage_count = usage_count + 1,
                 ${result === 'success' ? 'success_count = success_count + 1' : 'failure_count = failure_count + 1'},
                 experience_points = ?,
                 proficiency_level = ?,
                 last_used_at = CURRENT_TIMESTAMP,
                 performance_metrics = ?
             WHERE id = ?`,
            [newXP, newLevel, JSON.stringify(metrics), skill.id]
        );

        // Record level up if applicable
        if (newLevel > oldLevel) {
            await this.db.run(
                `INSERT INTO memory_evolution_history (skill_id, old_level, new_level, reason)
                 VALUES (?, ?, ?, ?)`,
                [skill.id, oldLevel, newLevel, `XP reached ${newXP}`]
            );
        }

        return {
            success: true,
            skillId: skill.id,
            xpGained: xpGain,
            totalXP: newXP,
            level: newLevel,
            leveledUp: newLevel > oldLevel
        };
    }

    /**
     * Calculate XP gain
     */
    calculateXP(result, metrics) {
        let baseXP = 10;
        
        if (result === 'success') {
            baseXP += 5;
        } else if (result === 'failure') {
            baseXP += 2; // Learning from failure
        }

        // Bonus for complexity
        if (metrics.complexity) {
            baseXP += metrics.complexity * 2;
        }

        // Bonus for time efficiency
        if (metrics.timeEfficiency) {
            baseXP += Math.floor(metrics.timeEfficiency / 10);
        }

        return baseXP;
    }

    /**
     * Calculate level from XP
     */
    calculateLevel(xp) {
        for (let level = 6; level >= 1; level--) {
            if (xp >= this.levelThresholds[level]) {
                return level;
            }
        }
        return 1;
    }

    /**
     * Get skill details
     */
    async getSkill(skillName) {
        const sql = `SELECT * FROM v_skill_summary WHERE skill_name = ?`;
        return await this.db.get(sql, [skillName]);
    }

    /**
     * Get all skills
     */
    async getAllSkills(category = null, limit = 50) {
        let sql = `SELECT * FROM v_skill_summary`;
        const params = [];

        if (category) {
            sql += ` WHERE skill_category = ?`;
            params.push(category);
        }

        sql += ` ORDER BY proficiency_level DESC, experience_points DESC LIMIT ?`;
        params.push(limit);

        return await this.db.all(sql, params);
    }

    /**
     * Get skills by category
     */
    async getByCategory(category) {
        const sql = `
            SELECT * FROM memory_evolution 
            WHERE skill_category = ? 
            ORDER BY proficiency_level DESC, experience_points DESC
        `;
        return await this.db.all(sql, [category]);
    }

    /**
     * Get skill history
     */
    async getSkillHistory(skillId) {
        const sql = `
            SELECT * FROM memory_evolution_history 
            WHERE skill_id = ? 
            ORDER BY created_at DESC
        `;
        return await this.db.all(sql, [skillId]);
    }

    /**
     * Get top skills
     */
    async getTopSkills(limit = 10) {
        const sql = `
            SELECT * FROM v_skill_summary 
            ORDER BY proficiency_level DESC, experience_points DESC 
            LIMIT ?
        `;
        return await this.db.all(sql, [limit]);
    }

    /**
     * Get skills needing improvement
     */
    async getNeedsImprovement(threshold = 50) {
        const sql = `
            SELECT * FROM v_skill_summary 
            WHERE success_rate < ? 
            ORDER BY success_rate ASC
        `;
        return await this.db.all(sql, [threshold]);
    }

    /**
     * Get category statistics
     */
    async getCategoryStats() {
        const sql = `
            SELECT 
                skill_category,
                COUNT(*) as skill_count,
                AVG(proficiency_level) as avg_level,
                SUM(experience_points) as total_xp,
                AVG(CAST(success_count AS REAL) / NULLIF(usage_count, 0) * 100) as avg_success_rate
            FROM memory_evolution 
            GROUP BY skill_category
        `;
        return await this.db.all(sql);
    }

    /**
     * Generate growth report
     */
    async generateGrowthReport(days = 30) {
        const sql = `
            SELECT 
                skill_name,
                proficiency_level,
                experience_points,
                usage_count,
                success_count,
                failure_count,
                last_used_at
            FROM memory_evolution 
            WHERE last_used_at >= datetime('now', '-${days} days')
            ORDER BY experience_points DESC
        `;

        const recentSkills = await this.db.all(sql);
        const categories = await this.getCategoryStats();

        return {
            period: `${days} days`,
            activeSkills: recentSkills.length,
            totalXP: recentSkills.reduce((sum, s) => sum + s.experience_points, 0),
            avgLevel: recentSkills.length > 0 
                ? recentSkills.reduce((sum, s) => sum + s.proficiency_level, 0) / recentSkills.length 
                : 0,
            topSkills: recentSkills.slice(0, 5),
            categoryBreakdown: categories
        };
    }

    /**
     * Get next milestone for skill
     */
    getNextMilestone(skill) {
        const currentLevel = skill.proficiency_level;
        const currentXP = skill.experience_points;

        if (currentLevel >= 6) {
            return { reachedMax: true };
        }

        const nextLevel = currentLevel + 1;
        const xpNeeded = this.levelThresholds[nextLevel] - currentXP;

        return {
            currentLevel,
            nextLevel,
            currentXP,
            xpNeeded,
            levelName: this.levelNames[nextLevel]
        };
    }

    /**
     * Suggest skills to practice
     */
    async suggestPractice() {
        // Get skills that haven't been used recently
        const sql = `
            SELECT * FROM memory_evolution 
            WHERE last_used_at IS NULL 
               OR last_used_at < datetime('now', '-7 days')
            ORDER BY proficiency_level ASC
            LIMIT 5
        `;
        return await this.db.all(sql);
    }
}

module.exports = EvolutionModule;