import { DialogueManager } from '../src/dialogue';
import { DialogueState, Model } from '../src/types';

describe('DialogueManager - 对话流程测试', () => {
  let dialogue: DialogueManager;

  beforeEach(() => {
    dialogue = new DialogueManager();
  });

  const mockModels: Model[] = [
    {
      id: '01',
      name: '第一性原理',
      category: 'core',
      description: '测试模型',
      questions: ['问题1', '问题2', '问题3'],
      scoring: { clear: '清晰', unclear: '不清晰' }
    },
    {
      id: '06',
      name: '能力圈',
      category: 'core',
      description: '测试模型',
      questions: ['问题A', '问题B'],
      scoring: { high: '高', low: '低' }
    }
  ];

  describe('会话创建', () => {
    test('应能创建新会话', () => {
      const context = dialogue.createSession('test-001', '测试决策');
      
      expect(context.sessionId).toBe('test-001');
      expect(context.userInput).toBe('测试决策');
      expect(context.state).toBe(DialogueState.START);
      expect(context.selectedModels).toHaveLength(0);
    });

    test('应能获取已创建的会话', () => {
      dialogue.createSession('test-002', '测试');
      const context = dialogue.getContext('test-002');
      
      expect(context).toBeDefined();
      expect(context?.sessionId).toBe('test-002');
    });

    test('获取不存在的会话应返回 undefined', () => {
      const context = dialogue.getContext('nonexistent');
      expect(context).toBeUndefined();
    });
  });

  describe('状态管理', () => {
    test('应能更新会话状态', () => {
      dialogue.createSession('test-003', '测试');
      dialogue.updateState('test-003', DialogueState.QUESTIONING);
      
      const context = dialogue.getContext('test-003');
      expect(context?.state).toBe(DialogueState.QUESTIONING);
    });

    test('应能设置场景', () => {
      dialogue.createSession('test-004', '测试');
      dialogue.setScenario('test-004', 'investment');
      
      const context = dialogue.getContext('test-004');
      expect(context?.scenario).toBe('investment');
    });

    test('应能设置模型列表', () => {
      dialogue.createSession('test-005', '测试');
      dialogue.setModels('test-005', ['01', '06', '07']);
      
      const context = dialogue.getContext('test-005');
      expect(context?.selectedModels).toEqual(['01', '06', '07']);
      expect(context?.currentModelIndex).toBe(0);
      expect(context?.currentQuestionIndex).toBe(0);
    });
  });

  describe('答案记录', () => {
    test('应能记录答案', () => {
      dialogue.createSession('test-006', '测试');
      dialogue.recordAnswer('test-006', '01', 0, '答案1');
      dialogue.recordAnswer('test-006', '01', 1, '答案2');
      
      const context = dialogue.getContext('test-006');
      expect(context?.answers['01']).toEqual(['答案1', '答案2']);
    });

    test('应能记录多个模型的答案', () => {
      dialogue.createSession('test-007', '测试');
      dialogue.recordAnswer('test-007', '01', 0, '模型1答案');
      dialogue.recordAnswer('test-007', '06', 0, '模型2答案');
      
      const context = dialogue.getContext('test-007');
      expect(context?.answers['01']).toEqual(['模型1答案']);
      expect(context?.answers['06']).toEqual(['模型2答案']);
    });
  });

  describe('问题导航', () => {
    test('应能移动到下一个问题', () => {
      dialogue.createSession('test-008', '测试');
      dialogue.setModels('test-008', ['01']);
      
      const hasNext = dialogue.nextQuestion('test-008', mockModels[0]);
      expect(hasNext).toBe(true);
      
      const context = dialogue.getContext('test-008');
      expect(context?.currentQuestionIndex).toBe(1);
    });

    test('当前模型问题完成后应移动到下一个模型', () => {
      dialogue.createSession('test-009', '测试');
      dialogue.setModels('test-009', ['01', '06']);
      
      // 完成第一个模型的所有问题
      dialogue.nextQuestion('test-009', mockModels[0]); // 问题1 -> 2
      dialogue.nextQuestion('test-009', mockModels[0]); // 问题2 -> 3
      const hasNext = dialogue.nextQuestion('test-009', mockModels[0]); // 问题3 -> 下一个模型
      
      expect(hasNext).toBe(true);
      const context = dialogue.getContext('test-009');
      expect(context?.currentModelIndex).toBe(1);
      expect(context?.currentQuestionIndex).toBe(0);
    });

    test('所有问题完成后应返回 false', () => {
      dialogue.createSession('test-010', '测试');
      dialogue.setModels('test-010', ['06']); // 只有2个问题
      
      dialogue.nextQuestion('test-010', mockModels[1]); // 问题A -> B
      const hasNext = dialogue.nextQuestion('test-010', mockModels[1]); // 问题B -> 完成
      
      expect(hasNext).toBe(false);
    });

    test('应能获取当前问题', () => {
      dialogue.createSession('test-011', '测试');
      dialogue.setModels('test-011', ['01', '06']);
      
      const current = dialogue.getCurrentQuestion('test-011', mockModels);
      expect(current).toBeDefined();
      expect(current?.model.id).toBe('01');
      expect(current?.question).toBe('问题1');
    });

    test('移动到下一个模型后应获取正确问题', () => {
      dialogue.createSession('test-012', '测试');
      dialogue.setModels('test-012', ['01', '06']);
      
      // 完成第一个模型
      dialogue.nextQuestion('test-012', mockModels[0]);
      dialogue.nextQuestion('test-012', mockModels[0]);
      dialogue.nextQuestion('test-012', mockModels[0]);
      
      const current = dialogue.getCurrentQuestion('test-012', mockModels);
      expect(current?.model.id).toBe('06');
      expect(current?.question).toBe('问题A');
    });
  });

  describe('会话清理', () => {
    test('应能删除会话', () => {
      dialogue.createSession('test-013', '测试');
      dialogue.deleteSession('test-013');
      
      const context = dialogue.getContext('test-013');
      expect(context).toBeUndefined();
    });

    test('应能清理过期会话', () => {
      dialogue.createSession('test-014', '测试');
      
      // 模拟过期（修改 updatedAt）
      const context = dialogue.getContext('test-014');
      if (context) {
        context.updatedAt = Date.now() - 25 * 60 * 60 * 1000; // 25小时前
      }
      
      dialogue.cleanupExpired();
      
      const afterCleanup = dialogue.getContext('test-014');
      expect(afterCleanup).toBeUndefined();
    });

    test('不应清理未过期的会话', () => {
      dialogue.createSession('test-015', '测试');
      dialogue.cleanupExpired();
      
      const context = dialogue.getContext('test-015');
      expect(context).toBeDefined();
    });
  });

  describe('完整对话流程', () => {
    test('应能完成完整的多轮对话', () => {
      // 1. 创建会话
      dialogue.createSession('test-016', '投资决策');
      
      // 2. 设置场景和模型
      dialogue.setScenario('test-016', 'investment');
      dialogue.setModels('test-016', ['01', '06']);
      dialogue.updateState('test-016', DialogueState.QUESTIONING);
      
      // 3. 回答第一个模型的问题
      let current = dialogue.getCurrentQuestion('test-016', mockModels);
      expect(current?.model.id).toBe('01');
      expect(current?.question).toBe('问题1');
      
      dialogue.recordAnswer('test-016', '01', 0, '答案1');
      dialogue.nextQuestion('test-016', mockModels[0]);
      
      current = dialogue.getCurrentQuestion('test-016', mockModels);
      expect(current?.question).toBe('问题2');
      
      dialogue.recordAnswer('test-016', '01', 1, '答案2');
      dialogue.nextQuestion('test-016', mockModels[0]);
      
      current = dialogue.getCurrentQuestion('test-016', mockModels);
      expect(current?.question).toBe('问题3');
      
      dialogue.recordAnswer('test-016', '01', 2, '答案3');
      dialogue.nextQuestion('test-016', mockModels[0]);
      
      // 4. 回答第二个模型的问题
      current = dialogue.getCurrentQuestion('test-016', mockModels);
      expect(current?.model.id).toBe('06');
      expect(current?.question).toBe('问题A');
      
      dialogue.recordAnswer('test-016', '06', 0, '答案A');
      dialogue.nextQuestion('test-016', mockModels[1]);
      
      current = dialogue.getCurrentQuestion('test-016', mockModels);
      expect(current?.question).toBe('问题B');
      
      dialogue.recordAnswer('test-016', '06', 1, '答案B');
      const hasNext = dialogue.nextQuestion('test-016', mockModels[1]);
      
      // 5. 验证完成
      expect(hasNext).toBe(false);
      
      const context = dialogue.getContext('test-016');
      expect(context?.answers['01']).toHaveLength(3);
      expect(context?.answers['06']).toHaveLength(2);
    });
  });
});
