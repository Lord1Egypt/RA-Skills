/**
 * Theme Module Loader - 主题模组加载器
 * 支持多主题自动加载与切换
 * 
 * v2.7.0 新增
 * 
 * 支持主题:
 * - wuxia (武侠)
 * - xianxia (修仙)
 * - medieval (中世纪)
 * - cyberpunk (赛博朋克)
 * - lovecraft (克苏鲁)
 * - shanghai (民国上海滩)
 */

const fs = require('fs');
const path = require('path');

// 主题枚举
const ThemeType = {
    WUXIA: 'wuxia',
    XIANXIA: 'xianxia',
    MEDIEVAL: 'medieval',
    CYBERPUNK: 'cyberpunk',
    LOVECRAFT: 'lovecraft',
    SHANGHAI: 'shanghai',
    BASE: 'base'
};

// 主题配置
const THEME_CONFIG = {
    [ThemeType.WUXIA]: {
        name: '武侠',
        displayName: '武侠世界',
        description: '刀光剑影的江湖世界',
        primaryColor: '#8B4513',
        secondaryColor: '#D2691E',
        keywords: ['武林', '江湖', '门派', '功法', '内力', '剑客', '侠客'],
        filePatterns: ['wuxia', '武侠', 'lingan'],
        cardCategories: ['role', 'location', 'item', 'event'],
        attributeScale: 'traditional' // 传统武侠数值
    },
    [ThemeType.XIANXIA]: {
        name: '修仙',
        displayName: '修仙世界',
        description: '仙道求真的玄幻世界',
        primaryColor: '#4B0082',
        secondaryColor: '#9370DB',
        keywords: ['修仙', '灵气', '功法', '境界', '法宝', '灵根', '炼丹'],
        filePatterns: ['xianxia', '修仙', '死灵'],
        cardCategories: ['role', 'location', 'item', 'event', 'state'],
        attributeScale: 'cultivation' // 修仙数值
    },
    [ThemeType.MEDIEVAL]: {
        name: '中世纪',
        displayName: '中世纪欧洲',
        description: '骑士与城堡的时代',
        primaryColor: '#2F4F4F',
        secondaryColor: '#708090',
        keywords: ['骑士', '城堡', '王国', '领主', '骑士团', '魔法'],
        filePatterns: ['medieval', '中世纪', '白银骑士'],
        cardCategories: ['role', 'location', 'item', 'event'],
        attributeScale: 'medieval'
    },
    [ThemeType.CYBERPUNK]: {
        name: '赛博朋克',
        displayName: '赛博朋克未来',
        description: '高科技与低生活的都市',
        primaryColor: '#00CED1',
        secondaryColor: '#FF00FF',
        keywords: ['义肢', 'AI', '公司', '黑客', '赛博格', '虚拟现实'],
        filePatterns: ['cyberpunk', '赛博', '热屋'],
        cardCategories: ['role', 'location', 'item', 'event'],
        attributeScale: 'cyber'
    },
    [ThemeType.LOVECRAFT]: {
        name: '克苏鲁',
        displayName: '克苏鲁神话',
        description: '克苏鲁神话主题',
        primaryColor: '#2F4F4F',
        secondaryColor: '#800080',
        keywords: ['邪神', '古神', '理智', '疯狂', '调查员', '神话生物'],
        filePatterns: ['lovecraft', '克苏鲁', 'coc', '针本'],
        cardCategories: ['role', 'location', 'item', 'event', 'state'],
        attributeScale: 'cosmic'
    },
    [ThemeType.SHANGHAI]: {
        name: '民国上海滩',
        displayName: '民国上海滩',
        description: '旧上海滩的恩怨情仇',
        primaryColor: '#B8860B',
        secondaryColor: '#DC143C',
        keywords: ['上海滩', '帮派', '军阀', '租界', '商人', '特工'],
        filePatterns: ['shanghai', '上海', '民国'],
        cardCategories: ['role', 'location', 'item', 'event'],
        attributeScale: 'modern'
    },
    [ThemeType.BASE]: {
        name: '基础',
        displayName: '基础世界',
        description: '通用基础设定',
        primaryColor: '#333333',
        secondaryColor: '#666666',
        keywords: ['基础', '通用'],
        cardCategories: ['role', 'location', 'item', 'state', 'event', 'ending'],
        attributeScale: 'base'
    }
};

/**
 * 主题模组类
 */
class ThemeModule {
    constructor(themeType, config) {
        this.type = themeType;
        this.config = config;
        this.data = {
            roles: [],
            locations: [],
            items: [],
            events: [],
            states: [],
            endings: [],
            rules: [],
            characters: [],
            maps: [],
            terms: []
        };
        this.loaded = false;
    }

    addData(category, items) {
        if (this.data[category]) {
            this.data[category] = [...this.data[category], ...items];
        }
    }

    getData(category) {
        return this.data[category] || [];
    }

    toJSON() {
        return {
            type: this.type,
            config: this.config,
            data: {
                rolesCount: this.data.roles.length,
                locationsCount: this.data.locations.length,
                itemsCount: this.data.items.length,
                eventsCount: this.data.events.length,
                statesCount: this.data.states.length,
                endingsCount: this.data.endings.length
            },
            loaded: this.loaded
        };
    }
}

/**
 * 主题模组加载器
 */
class ThemeModuleLoader {
    constructor(dataDir = null) {
        this.dataDir = dataDir || path.join(__dirname, '..', 'data');
        this.themes = new Map();
        this.currentTheme = null;
        this.fallbackTheme = ThemeType.BASE;
        
        // 初始化所有主题
        this._initThemes();
    }

    // 初始化主题配置
    _initThemes() {
        for (const [type, config] of Object.entries(THEME_CONFIG)) {
            this.themes.set(type, new ThemeModule(type, config));
        }
    }

    // 获取所有可用主题
    getAvailableThemes() {
        const themeList = [];
        for (const [type, module] of this.themes) {
            if (type !== ThemeType.BASE) {
                themeList.push({
                    type,
                    name: module.config.name,
                    displayName: module.config.displayName,
                    description: module.config.description,
                    loaded: module.loaded
                });
            }
        }
        return themeList;
    }

    // 获取主题配置
    getThemeConfig(themeType) {
        return THEME_CONFIG[themeType] || THEME_CONFIG[ThemeType.BASE];
    }

    // 获取当前主题
    getCurrentTheme() {
        return this.currentTheme;
    }

    // 获取主题模块
    getThemeModule(themeType) {
        return this.themes.get(themeType);
    }

    // 验证主题是否存在
    validateTheme(themeType) {
        if (this.themes.has(themeType)) {
            return { valid: true };
        }
        
        // 尝试模糊匹配
        const lowerTheme = themeType.toLowerCase();
        for (const [type, config] of Object.entries(THEME_CONFIG)) {
            if (config.name.includes(lowerTheme) || 
                config.displayName.includes(lowerTheme) ||
                type.includes(lowerTheme)) {
                return { valid: true, matchedType: type };
            }
        }
        
        return { 
            valid: false, 
            available: this.getAvailableThemes().map(t => t.type),
            fallback: this.fallbackTheme
        };
    }

    // 加载主题数据
    async loadTheme(themeType) {
        // 验证主题
        const validation = this.validateTheme(themeType);
        if (!validation.valid) {
            return {
                success: false,
                error: `主题 "${themeType}" 不存在`,
                suggestion: validation,
                fallback: this.fallbackTheme
            };
        }

        // 使用匹配的主题
        const actualType = validation.matchedType || themeType;
        const themeModule = this.themes.get(actualType);

        // 如果已加载，直接返回
        if (themeModule.loaded) {
            this.currentTheme = themeModule;
            return {
                success: true,
                message: `主题 "${themeModule.config.displayName}" 已加载`,
                theme: themeModule.toJSON()
            };
        }

        // 加载主题数据
        try {
            await this._loadThemeData(themeModule);
            themeModule.loaded = true;
            this.currentTheme = themeModule;

            return {
                success: true,
                message: `主题 "${themeModule.config.displayName}" 加载成功`,
                theme: themeModule.toJSON()
            };
        } catch (error) {
            console.error(`加载主题 ${themeType} 失败:`, error);
            
            // 回退到基础主题
            const fallbackModule = this.themes.get(this.fallbackTheme);
            this.currentTheme = fallbackModule;
            
            return {
                success: false,
                error: error.message,
                fallback: this.fallbackTheme,
                fallbackTheme: fallbackModule.toJSON()
            };
        }
    }

    // 加载主题数据（从文件）
    async _loadThemeData(themeModule) {
        const config = themeModule.config;
        
        // 尝试从多个文件模式加载
        const filePatterns = config.filePatterns;
        
        for (const pattern of filePatterns) {
            try {
                await this._loadFromPattern(themeModule, pattern);
            } catch (e) {
                // 继续尝试下一个模式
            }
        }

        // 如果没有加载到任何数据，尝试加载通用数据
        if (!themeModule.data.roles.length && !themeModule.data.locations.length) {
            await this._loadBaseData(themeModule);
        }
    }

    // 从特定模式加载数据
    async _loadFromPattern(themeModule, pattern) {
        // 扫描data目录中的文件
        const files = fs.readdirSync(this.dataDir);
        
        for (const file of files) {
            if (!file.endsWith('.json')) continue;
            
            const filePath = path.join(this.dataDir, file);
            const content = fs.readFileSync(filePath, 'utf-8');
            const data = JSON.parse(content);
            
            // 检查文件是否匹配主题
            const fileName = file.toLowerCase();
            if (!fileName.includes(pattern.toLowerCase())) continue;
            
            // 解析数据
            this._parseThemeData(themeModule, data);
        }
    }

    // 解析主题数据
    _parseThemeData(themeModule, data) {
        // 角色数据
        if (data.跑团模组 || data.角色记录) {
            const roles = this._extractRoles(data);
            themeModule.addData('roles', roles);
        }

        // 地点数据
        if (data.地图) {
            const locations = this._extractLocations(data);
            themeModule.addData('locations', locations);
        }

        // 基础卡牌数据
        if (data.基础卡库) {
            const cards = this._extractBaseCards(data);
            themeModule.addData('items', cards.items);
            themeModule.addData('locations', cards.locations);
            themeModule.addData('events', cards.events);
        }

        // 词条数据
        if (data.词条) {
            const terms = this._extractTerms(data);
            themeModule.addData('terms', terms);
        }

        // 克苏鲁大纲
        if (data.大纲) {
            const events = this._extractCthulhuEvents(data);
            themeModule.addData('events', events);
        }

        // 规则数据
        if (data.规则修改记录) {
            themeModule.addData('rules', data.规则修改记录);
        }

        // 通用结局
        if (data.通用结局) {
            themeModule.addData('endings', data.通用结局);
        }
    }

    // 提取角色数据
    _extractRoles(data) {
        const roles = [];
        
        // 从角色记录提取
        if (data.角色记录) {
            const records = Array.isArray(data.角色记录) ? data.角色记录 : [data.角色记录];
            for (const record of records) {
                if (record.Unnamed_1 || record['角色']) {
                    roles.push({
                        id: `role_${roles.length + 1}`,
                        name: record.Unnamed_1 || record['角色'] || record.Unnamed_2,
                        type: 'role',
                        description: record.经历 || record.Unnamed_3 || '',
                        attributes: {
                            生命: record.Unnamed_2 || 10,
                            攻击: record.Unnamed_3 || 3,
                            防守: record.Unnamed_4 || 3,
                            速度: record.Unnamed_5 || 3
                        }
                    });
                }
            }
        }

        // 从跑团模组提取
        if (data.跑团模组) {
            const modules = Array.isArray(data.跑团模组) ? data.跑团模组 : [];
            for (const mod of modules) {
                if (mod.Unnamed_2) {
                    roles.push({
                        id: `module_${roles.length + 1}`,
                        name: mod.Unnamed_2,
                        type: 'module_role',
                        description: mod.Unnamed_3 || '',
                        tags: mod.Unnamed_14 ? mod.Unnamed_14.split(' ') : []
                    });
                }
            }
        }

        return roles;
    }

    // 提取地点数据
    _extractLocations(data) {
        const locations = [];
        
        if (data.地图) {
            const mapData = Array.isArray(data.地图) ? data.地图 : [data.地图];
            for (const loc of mapData) {
                const name = loc.Unnamed_8 || loc['色块定义'] || '';
                if (name) {
                    locations.push({
                        id: `loc_${locations.length + 1}`,
                        name,
                        type: 'location',
                        action: loc['色块行动规则'] || '',
                        extra: loc.Unnamed_14 || ''
                    });
                }
            }
        }

        return locations;
    }

    // 提取基础卡牌
    _extractBaseCards(data) {
        const items = [];
        const locations = [];
        const events = [];

        if (data.基础卡库) {
            const cards = Array.isArray(data.基础卡库) ? data.基础卡库 : [data.基础卡库];
            for (const card of cards) {
                if (card['角色（生物）']) {
                    items.push({
                        id: `item_${items.length + 1}`,
                        name: card['角色（生物）'],
                        type: 'role',
                        category: 'character'
                    });
                }
                if (card['地点']) {
                    locations.push({
                        id: `loc_${locations.length + 1}`,
                        name: card['地点'],
                        type: 'location'
                    });
                }
                if (card['物品']) {
                    items.push({
                        id: `item_${items.length + 1}`,
                        name: card['物品'],
                        type: 'item'
                    });
                }
                if (card['状态']) {
                    items.push({
                        id: `state_${items.length + 1}`,
                        name: card['状态'],
                        type: 'state'
                    });
                }
                if (card['事件']) {
                    events.push({
                        id: `event_${events.length + 1}`,
                        name: card['事件'],
                        type: 'event'
                    });
                }
            }
        }

        return { items, locations, events };
    }

    // 提取词条
    _extractTerms(data) {
        const terms = [];
        
        if (data.词条) {
            const termList = Array.isArray(data.词条) ? data.词条 : [data.词条];
            for (const term of termList) {
                if (term['角色'] || term.Unnamed_2) {
                    terms.push({
                        id: `term_${terms.length + 1}`,
                        role: term['角色'] || term.Unnamed_2,
                        location: term['地点'] || term.Unnamed_3,
                        item: term['物品'] || term.Unnamed_4,
                        state: term['状态'] || term.Unnamed_5,
                        event: term['事件'] || term.Unnamed_6,
                        ending: term['结局'] || term.Unnamed_7,
                        style: term['画风'] || term.Unnamed_8
                    });
                }
            }
        }

        return terms;
    }

    // 提取克苏鲁事件
    _extractCthulhuEvents(data) {
        const events = [];
        
        if (data.大纲) {
            const outline = Array.isArray(data.大纲) ? data.大纲 : [data.大纲];
            for (const item of outline) {
                if (item['编号'] || item.Unnamed_1) {
                    events.push({
                        id: `cthulhu_${events.length + 1}`,
                        number: item['编号'] || item.Unnamed_1,
                        title: item['目录'] || item.Unnamed_2,
                        theme: item['主题'] || item.Unnamed_3,
                        coreTransform: item['核心转换'] || item.Unnamed_4,
                        coreTrick: item['核心诡计'] || item.Unnamed_5
                    });
                }
            }
        }

        return events;
    }

    // 加载基础数据
    async _loadBaseData(themeModule) {
        // 尝试加载通用数据文件
        const baseFiles = ['game-design-source.json', 'zhenben_module.json'];
        
        for (const file of baseFiles) {
            const filePath = path.join(this.dataDir, file);
            if (fs.existsSync(filePath)) {
                const content = fs.readFileSync(filePath, 'utf-8');
                const data = JSON.parse(content);
                this._parseThemeData(themeModule, data);
            }
        }
    }

    // 切换主题
    async switchTheme(themeType) {
        return this.loadTheme(themeType);
    }

    // 获取当前主题数据
    getCurrentThemeData(category = null) {
        if (!this.currentTheme) {
            return null;
        }
        
        if (category) {
            return this.currentTheme.getData(category);
        }
        
        return this.currentTheme.data;
    }

    // 获取主题特定的卡牌数据
    getThemeCards(themeType = null) {
        const targetTheme = themeType ? this.themes.get(themeType) : this.currentTheme;
        if (!targetTheme) return [];

        return {
            roles: targetTheme.data.roles,
            locations: targetTheme.data.locations,
            items: targetTheme.data.items,
            events: targetTheme.data.events,
            terms: targetTheme.data.terms
        };
    }

    // 验证主题兼容性
    validateCompatibility(themeType) {
        const theme = this.themes.get(themeType);
        if (!theme) {
            return { compatible: false, reason: '主题不存在' };
        }

        const issues = [];
        
        // 检查数据完整性
        const totalData = Object.values(theme.data).reduce((sum, arr) => sum + arr.length, 0);
        if (totalData < 10) {
            issues.push('数据量较少');
        }

        return {
            compatible: issues.length === 0,
            issues,
            dataSummary: {
                roles: theme.data.roles.length,
                locations: theme.data.locations.length,
                items: theme.data.items.length,
                events: theme.data.events.length,
                terms: theme.data.terms.length
            }
        };
    }

    // 生成主题报告
    generateThemeReport(themeType = null) {
        const targetTheme = themeType ? this.themes.get(themeType) : this.currentTheme;
        if (!targetTheme) {
            return { error: '没有加载的主题' };
        }

        const config = targetTheme.config;
        const data = targetTheme.data;

        return {
            theme: {
                type: targetTheme.type,
                name: config.name,
                displayName: config.displayName,
                description: config.description,
                loaded: targetTheme.loaded
            },
            statistics: {
                totalRoles: data.roles.length,
                totalLocations: data.locations.length,
                totalItems: data.items.length,
                totalEvents: data.events.length,
                totalTerms: data.terms.length,
                totalRules: data.rules.length,
                totalEndings: data.endings.length
            },
            keywords: config.keywords,
            cardCategories: config.cardCategories,
            attributeScale: config.attributeScale
        };
    }

    // 重置到基础主题
    resetToBase() {
        this.currentTheme = this.themes.get(ThemeType.BASE);
        return {
            success: true,
            message: '已重置到基础主题',
            theme: this.currentTheme.toJSON()
        };
    }

    // 导出主题配置（用于保存/加载）
    exportConfig() {
        return {
            currentTheme: this.currentTheme ? this.currentTheme.type : null,
            availableThemes: this.getAvailableThemes(),
            exportedAt: new Date().toISOString()
        };
    }
}

// 导出
module.exports = {
    ThemeModuleLoader,
    ThemeModule,
    ThemeType,
    THEME_CONFIG
};

// 命令行测试
if (require.main === module) {
    console.log('🎨 Theme Module Loader v2.7.0');
    console.log('='.repeat(50));
    
    const loader = new ThemeModuleLoader();
    
    // 显示可用主题
    console.log('\n📋 可用主题:');
    const themes = loader.getAvailableThemes();
    themes.forEach(t => {
        console.log(`  - ${t.type}: ${t.displayName} (${t.description})`);
    });
    
    // 测试加载武侠主题
    console.log('\n🗡️ 加载武侠主题...');
    const wuxiaResult = loader.loadTheme('wuxia');
    console.log(wuxiaResult.message);
    if (wuxiaResult.success) {
        console.log('📊 主题统计:', wuxiaResult.theme);
    }
    
    // 测试主题报告
    console.log('\n📝 主题报告:');
    const report = loader.generateThemeReport();
    console.log(JSON.stringify(report, null, 2));
    
    // 测试加载克苏鲁主题
    console.log('\n🦑 加载克苏鲁主题...');
    const lovecraftResult = loader.loadTheme('lovecraft');
    console.log(lovecraftResult.message);
    if (lovecraftResult.success) {
        const lovecraftReport = loader.generateThemeReport('lovecraft');
        console.log('克苏鲁统计:', lovecraftReport.statistics);
    }
    
    // 测试主题切换
    console.log('\n🔄 测试主题切换...');
    const switchResult = loader.switchTheme('shanghai');
    console.log(switchResult.message);
    
    // 测试验证
    console.log('\n✅ 验证主题...');
    console.log('wuxia:', loader.validateCompatibility('wuxia'));
    console.log('invalid:', loader.validateTheme('invalid_theme'));
    
    console.log('\n✅ 主题模组加载器测试完成!');
}
