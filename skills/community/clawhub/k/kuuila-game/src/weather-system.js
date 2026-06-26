/**
 * Weather System - 天气系统
 * v2.4 城主规则系统组件
 * 
 * 功能：
 * - 天气判定系统
 * - 影响移动规则
 * - 天气事件触发
 */

/**
 * 天气类型枚举
 */
const WeatherType = {
    SUNNY: 'sunny',       // 晴天
    CLOUDY: 'cloudy',     // 阴天
    RAINY: 'rainy',       // 雨天
    STORMY: 'stormy',     // 暴风雨
    FOGGY: 'foggy',       // 迷雾
    SNOWY: 'snowy'        // 雪天
};

/**
 * 天气效果配置
 */
const WEATHER_EFFECTS = {
    [WeatherType.SUNNY]: {
        name: '晴天',
        icon: '☀️',
        description: '阳光明媚，行动顺利',
        moveModifier: 0,        // 移动消耗修正
        visionModifier: 0,      // 视野修正
        eventBonus: [],         // 事件加成
        specialRules: []
    },
    [WeatherType.CLOUDY]: {
        name: '阴天',
        icon: '☁️',
        description: '阴云密布，气氛压抑',
        moveModifier: 0,
        visionModifier: -1,
        eventBonus: ['神秘事件概率+10%'],
        specialRules: []
    },
    [WeatherType.RAINY]: {
        name: '雨天',
        icon: '🌧️',
        description: '细雨绵绵，行动受阻',
        moveModifier: 1,         // 移动消耗+1
        visionModifier: -1,
        eventBonus: ['潜行效果+20%'],
        specialRules: ['河流移动需额外判定']
    },
    [WeatherType.STORMY]: {
        name: '暴风雨',
        icon: '⛈️',
        description: '狂风暴雨，危险重重',
        moveModifier: 2,         // 移动消耗+2
        visionModifier: -2,
        eventBonus: ['神秘事件概率+30%', '危险事件概率+20%'],
        specialRules: ['河流移动必须判定，失败则漂流', '室外行动消耗翻倍']
    },
    [WeatherType.FOGGY]: {
        name: '迷雾',
        icon: '🌫️',
        description: '浓雾弥漫，方向难辨',
        moveModifier: 0,
        visionModifier: -3,
        eventBonus: ['迷路概率+40%', '神秘相遇+30%'],
        specialRules: ['移动方向可能偏移', '隐藏地点更难发现']
    },
    [WeatherType.SNOWY]: {
        name: '雪天',
        icon: '❄️',
        description: '雪花飘落，银装素裹',
        moveModifier: 1,
        visionModifier: -1,
        eventBonus: ['治愈效果+20%'],
        specialRules: ['足迹可见', '保暖消耗']
    }
};

/**
 * 天气系统类
 */
class WeatherSystem {
    constructor() {
        this.currentWeather = WeatherType.SUNNY;
        this.weatherHistory = [];
        this.weatherDuration = 0;
        this.forecast = [];
        
        // 天气转换概率矩阵
        this.transitionMatrix = {
            [WeatherType.SUNNY]: {
                [WeatherType.SUNNY]: 0.5,
                [WeatherType.CLOUDY]: 0.3,
                [WeatherType.RAINY]: 0.1,
                [WeatherType.STORMY]: 0.0,
                [WeatherType.FOGGY]: 0.05,
                [WeatherType.SNOWY]: 0.05
            },
            [WeatherType.CLOUDY]: {
                [WeatherType.SUNNY]: 0.2,
                [WeatherType.CLOUDY]: 0.4,
                [WeatherType.RAINY]: 0.25,
                [WeatherType.STORMY]: 0.05,
                [WeatherType.FOGGY]: 0.05,
                [WeatherType.SNOWY]: 0.05
            },
            [WeatherType.RAINY]: {
                [WeatherType.SUNNY]: 0.1,
                [WeatherType.CLOUDY]: 0.3,
                [WeatherType.RAINY]: 0.35,
                [WeatherType.STORMY]: 0.15,
                [WeatherType.FOGGY]: 0.05,
                [WeatherType.SNOWY]: 0.05
            },
            [WeatherType.STORMY]: {
                [WeatherType.SUNNY]: 0.05,
                [WeatherType.CLOUDY]: 0.25,
                [WeatherType.RAINY]: 0.4,
                [WeatherType.STORMY]: 0.2,
                [WeatherType.FOGGY]: 0.05,
                [WeatherType.SNOWY]: 0.05
            },
            [WeatherType.FOGGY]: {
                [WeatherType.SUNNY]: 0.3,
                [WeatherType.CLOUDY]: 0.3,
                [WeatherType.RAINY]: 0.1,
                [WeatherType.STORMY]: 0.0,
                [WeatherType.FOGGY]: 0.25,
                [WeatherType.SNOWY]: 0.05
            },
            [WeatherType.SNOWY]: {
                [WeatherType.SUNNY]: 0.2,
                [WeatherType.CLOUDY]: 0.3,
                [WeatherType.RAINY]: 0.1,
                [WeatherType.STORMY]: 0.0,
                [WeatherType.FOGGY]: 0.2,
                [WeatherType.SNOWY]: 0.2
            }
        };
    }

    /**
     * 河流天气判定 (v1.2规则: 1-3阴天/4-6晴天)
     * @returns {Object} 判定结果
     */
    rollRiverWeather() {
        const roll = this._rollD6();
        const isSunny = roll >= 4;
        
        const result = {
            roll,
            weather: isSunny ? WeatherType.SUNNY : WeatherType.CLOUDY,
            isSunny,
            effect: WEATHER_EFFECTS[isSunny ? WeatherType.SUNNY : WeatherType.CLOUDY],
            message: `🎲 河流天气判定: ${roll}点 → ${isSunny ? '☀️ 晴天' : '☁️ 阴天'}`
        };
        
        return result;
    }

    /**
     * 判定天气变化
     * @param {boolean} forced 是否强制变化
     * @returns {Object} 新天气信息
     */
    rollWeatherChange(forced = false) {
        // 记录历史
        this.weatherHistory.push({
            weather: this.currentWeather,
            duration: this.weatherDuration,
            timestamp: Date.now()
        });
        
        if (forced || this._shouldChangeWeather()) {
            this.currentWeather = this._selectNextWeather();
            this.weatherDuration = 0;
        } else {
            this.weatherDuration++;
        }
        
        return {
            weather: this.currentWeather,
            effect: WEATHER_EFFECTS[this.currentWeather],
            duration: this.weatherDuration,
            message: `天气: ${WEATHER_EFFECTS[this.currentWeather].icon} ${WEATHER_EFFECTS[this.currentWeather].name}`
        };
    }

    /**
     * 设置指定天气
     * @param {string} weatherType 天气类型
     */
    setWeather(weatherType) {
        if (!WEATHER_EFFECTS[weatherType]) {
            return { error: `未知天气类型: ${weatherType}` };
        }
        
        this.weatherHistory.push({
            weather: this.currentWeather,
            duration: this.weatherDuration,
            timestamp: Date.now()
        });
        
        this.currentWeather = weatherType;
        this.weatherDuration = 0;
        
        return {
            success: true,
            weather: this.currentWeather,
            effect: WEATHER_EFFECTS[this.currentWeather],
            message: `天气已设为: ${WEATHER_EFFECTS[this.currentWeather].icon} ${WEATHER_EFFECTS[this.currentWeather].name}`
        };
    }

    /**
     * 获取当前天气效果
     * @returns {Object} 天气效果
     */
    getCurrentWeatherEffect() {
        return {
            weather: this.currentWeather,
            ...WEATHER_EFFECTS[this.currentWeather],
            duration: this.weatherDuration
        };
    }

    /**
     * 计算移动消耗
     * @param {string} terrainType 地形类型
     * @param {number} baseCost 基础消耗
     * @returns {Object} 计算结果
     */
    calculateMoveCost(terrainType, baseCost = 1) {
        const effect = WEATHER_EFFECTS[this.currentWeather];
        let modifiedCost = baseCost + effect.moveModifier;
        let reasons = [];
        
        if (effect.moveModifier !== 0) {
            reasons.push(`天气修正: ${effect.moveModifier > 0 ? '+' : ''}${effect.moveModifier}`);
        }
        
        // 地形特殊规则
        if (terrainType === 'river' || terrainType === 'water') {
            if (this.currentWeather === WeatherType.STORMY) {
                modifiedCost *= 2;
                reasons.push('暴风雨中河流移动消耗翻倍');
            }
        }
        
        if (terrainType === 'outdoor') {
            if (this.currentWeather === WeatherType.STORMY) {
                modifiedCost *= 2;
                reasons.push('暴风雨中室外行动消耗翻倍');
            }
        }
        
        return {
            baseCost,
            modifiedCost: Math.max(1, modifiedCost),
            weather: this.currentWeather,
            weatherName: effect.name,
            reasons,
            message: `移动消耗: ${baseCost} → ${modifiedCost} (天气影响)`
        };
    }

    /**
     * 判定特殊天气事件
     * @returns {Object|null} 特殊事件
     */
    checkWeatherEvent() {
        const effect = WEATHER_EFFECTS[this.currentWeather];
        
        // 根据天气类型触发不同概率的事件
        const eventChance = {
            [WeatherType.SUNNY]: 0,
            [WeatherType.CLOUDY]: 0.1,
            [WeatherType.RAINY]: 0.15,
            [WeatherType.STORMY]: 0.3,
            [WeatherType.FOGGY]: 0.25,
            [WeatherType.SNOWY]: 0.1
        };
        
        if (Math.random() < eventChance[this.currentWeather]) {
            return this._generateWeatherEvent();
        }
        
        return null;
    }

    /**
     * 生成天气预报
     * @param {number} turns 预报回合数
     * @returns {Array} 预报列表
     */
    generateForecast(turns = 3) {
        this.forecast = [];
        let tempWeather = this.currentWeather;
        
        for (let i = 0; i < turns; i++) {
            tempWeather = this._selectNextWeather(tempWeather);
            this.forecast.push({
                turn: i + 1,
                weather: tempWeather,
                ...WEATHER_EFFECTS[tempWeather]
            });
        }
        
        return this.forecast;
    }

    /**
     * 获取天气对行动的影响描述
     * @param {string} actionType 行动类型
     * @returns {Object} 影响描述
     */
    getActionImpact(actionType) {
        const effect = WEATHER_EFFECTS[this.currentWeather];
        const impacts = {
            canProceed: true,
            modifiers: [],
            warnings: [],
            bonuses: []
        };
        
        // 视野影响
        if (effect.visionModifier < 0) {
            impacts.modifiers.push({
                type: 'vision',
                value: effect.visionModifier,
                description: `视野范围减少 ${Math.abs(effect.visionModifier)} 格`
            });
        }
        
        // 特殊规则
        effect.specialRules.forEach(rule => {
            impacts.warnings.push(rule);
        });
        
        // 事件加成
        effect.eventBonus.forEach(bonus => {
            impacts.bonuses.push(bonus);
        });
        
        // 特定行动影响
        if (actionType === 'scout' && this.currentWeather === WeatherType.FOGGY) {
            impacts.modifiers.push({
                type: 'scout',
                value: -2,
                description: '迷雾中侦察效果降低'
            });
        }
        
        if (actionType === 'stealth' && this.currentWeather === WeatherType.RAINY) {
            impacts.bonuses.push('雨天掩护，潜行效果+20%');
        }
        
        if (actionType === 'travel' && this.currentWeather === WeatherType.STORMY) {
            impacts.warnings.push('暴风雨中旅行风险极高，建议寻找避难所');
        }
        
        return impacts;
    }

    // 私有方法

    /**
     * 投掷D6骰子
     */
    _rollD6() {
        return Math.floor(Math.random() * 6) + 1;
    }

    /**
     * 判断是否应该变化天气
     */
    _shouldChangeWeather() {
        // 持续时间越长，变化概率越高
        const changeChance = Math.min(0.8, 0.2 + this.weatherDuration * 0.15);
        return Math.random() < changeChance;
    }

    /**
     * 选择下一个天气
     */
    _selectNextWeather(current = this.currentWeather) {
        const transitions = this.transitionMatrix[current];
        const rand = Math.random();
        let cumulative = 0;
        
        for (const [weather, probability] of Object.entries(transitions)) {
            cumulative += probability;
            if (rand < cumulative) {
                return weather;
            }
        }
        
        return current; // 默认保持当前天气
    }

    /**
     * 生成天气事件
     */
    _generateWeatherEvent() {
        const events = {
            [WeatherType.STORMY]: [
                { type: 'hazard', name: '雷电袭击', damage: 2, description: '一道闪电劈向附近' },
                { type: 'obstacle', name: '树木倒塌', description: '暴风雨中一棵大树倒下，阻挡了道路' },
                { type: 'discovery', name: '雨中遗物', description: '暴风雨冲刷出了被掩埋的物品' }
            ],
            [WeatherType.FOGGY]: [
                { type: 'lost', name: '迷失方向', description: '浓雾中你失去了方向感' },
                { type: 'encounter', name: '迷雾身影', description: '雾中出现了一个模糊的身影' },
                { type: 'discovery', name: '隐秘小径', description: '迷雾中你意外发现了一条隐蔽的小路' }
            ],
            [WeatherType.RAINY]: [
                { type: 'shelter', name: '避雨发现', description: '躲雨时发现了一个隐蔽的地方' },
                { type: 'track', name: '雨水冲刷', description: '雨水冲刷出了地面上的痕迹' }
            ],
            [WeatherType.CLOUDY]: [
                { type: 'omen', name: '乌云预兆', description: '阴沉的天空似乎预示着什么' }
            ],
            [WeatherType.SNOWY]: [
                { type: 'track', name: '雪地足迹', description: '雪地上清晰可见一串足迹' },
                { type: 'shelter', name: '雪中暖屋', description: '风雪中发现了一间温暖的小屋' }
            ]
        };
        
        const weatherEvents = events[this.currentWeather] || [];
        if (weatherEvents.length > 0) {
            return weatherEvents[Math.floor(Math.random() * weatherEvents.length)];
        }
        
        return null;
    }

    /**
     * 获取天气状态摘要
     */
    getSummary() {
        const effect = WEATHER_EFFECTS[this.currentWeather];
        return {
            current: {
                type: this.currentWeather,
                name: effect.name,
                icon: effect.icon,
                description: effect.description,
                duration: this.weatherDuration
            },
            effects: {
                moveModifier: effect.moveModifier,
                visionModifier: effect.visionModifier,
                specialRules: effect.specialRules,
                eventBonus: effect.eventBonus
            },
            forecast: this.forecast.slice(0, 2) // 只显示前2个预报
        };
    }

    /**
     * 重置天气系统
     */
    reset() {
        this.currentWeather = WeatherType.SUNNY;
        this.weatherHistory = [];
        this.weatherDuration = 0;
        this.forecast = [];
        
        return {
            success: true,
            message: '天气系统已重置为晴天'
        };
    }
}

// 导出
module.exports = {
    WeatherSystem,
    WeatherType,
    WEATHER_EFFECTS
};
