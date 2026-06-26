/**
 * Puzzle Game - 猜谜游戏模块
 * 支持传统谜语、脑筋急转弯、知识问答
 */

class PuzzleGame {
    constructor() {
        this.type = 'puzzle';
        this.score = 0;
        this.currentPuzzle = null;
        this.history = [];
    }

    // 游戏开始
    start(puzzleType = 'mixed') {
        this.puzzleType = puzzleType;
        return {
            message: '🎯 猜谜游戏开始！',
            type: puzzleType,
            instruction: '输入"出题"开始，输入"退出"结束游戏'
        };
    }

    // 获取谜题
    getPuzzle(type = 'mixed') {
        const puzzles = {
            traditional: [
                {
                    question: '有城不能住，有树不能遮，有河不能游，有山不能爬。打一物',
                    answer: '地图',
                    hint: '这东西您每天都在用，跟纸张有关',
                    difficulty: 2
                },
                {
                    question: '远看像座山，近看不是山，上边水直流，下边有人走。打一物',
                    answer: '伞',
                    hint: '下雨天用的',
                    difficulty: 2
                },
                {
                    question: '有嘴不能说，有腿不能行，有床不能睡。打一物',
                    answer: '河流',
                    hint: '自然地理',
                    difficulty: 3
                },
                {
                    question: '白天天上挂，晚上不见了，发光又发热，万物都需要。打一自然物',
                    answer: '太阳',
                    hint: '天上',
                    difficulty: 1
                }
            ],
            brain: [
                {
                    question: '什么东西越洗越脏？',
                    answer: '水',
                    hint: '日常生活中',
                    difficulty: 2
                },
                {
                    question: '什么门永远关不上？',
                    answer: '球门',
                    hint: '体育运动',
                    difficulty: 2
                },
                {
                    question: '什么人一年只工作一天？',
                    answer: '圣诞老人',
                    hint: '西方节日',
                    difficulty: 2
                }
            ],
            knowledge: [
                {
                    question: '三国演义中，刘备的字是什么？',
                    answer: '玄德',
                    hint: '刘玄德',
                    difficulty: 2
                },
                {
                    question: '中国历史上第一个皇帝是谁？',
                    answer: '秦始皇',
                    hint: '统一六国',
                    difficulty: 1
                },
                {
                    question: '《道德经》的作者是谁？',
                    answer: '老子',
                    hint: '道家创始人',
                    difficulty: 1
                }
            ]
        };

        // 混合模式
        if (type === 'mixed') {
            const allPuzzles = [
                ...puzzles.traditional,
                ...puzzles.brain,
                ...puzzles.knowledge
            ];
            return allPuzzles[Math.floor(Math.random() * allPuzzles.length)];
        }

        const typePuzzles = puzzles[type] || puzzles.traditional;
        return typePuzzles[Math.floor(Math.random() * typePuzzles.length)];
    }

    // 处理答案
    checkAnswer(answer, puzzle) {
        const isCorrect = answer.trim().toLowerCase() === puzzle.answer.trim().toLowerCase();
        
        if (isCorrect) {
            this.score += 10;
            return {
                correct: true,
                message: '✅ 恭喜您，答对了！',
                score: this.score
            };
        } else {
            return {
                correct: false,
                message: '❌ 不对哦，再想想～',
                hint: puzzle.hint
            };
        }
    }

    // 获取游戏状态
    getState() {
        return {
            type: this.type,
            score: this.score,
            puzzleType: this.puzzleType,
            history: this.history.length
        };
    }

    // 重置游戏
    reset() {
        this.score = 0;
        this.currentPuzzle = null;
        this.history = [];
    }
}

module.exports = { PuzzleGame };
