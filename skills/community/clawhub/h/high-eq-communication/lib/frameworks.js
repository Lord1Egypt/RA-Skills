/**
 * High-EQ Communication Frameworks (三语)
 * 高情商沟通框架数据
 */

const frameworks = {
  // ═══════════════════════════════════════════════
  // 非暴力沟通 (NVC)
  // ═══════════════════════════════════════════════
  nvc: {
    name: { en: 'Nonviolent Communication', zh: '非暴力沟通', ja: '非暴力コミュニケーション' },
    author: 'Marshall Rosenberg',
    steps: [
      { en: 'Observation', zh: '观察', ja: '観察', desc_en: 'State objective facts without judgment', desc_zh: '陈述客观事实，不加评判', desc_ja: '客観的な事実を判断せずに述べる' },
      { en: 'Feeling', zh: '感受', ja: '感情', desc_en: 'Express emotional response', desc_zh: '表达情绪反应', desc_ja: '感情的な反応を表現する' },
      { en: 'Need', zh: '需要', ja: '必要', desc_en: 'Identify underlying desire', desc_zh: '识别深层需求', desc_ja: '根底にある欲求を特定する' },
      { en: 'Request', zh: '请求', ja: '要求', desc_en: 'Make specific, actionable request', desc_zh: '提出具体可执行的请求', desc_ja: '具体的で実行可能な要求をする' },
    ],
    scenarios: [
      {
        en: 'Client is angry', zh: '客户愤怒', ja: 'クライアントが怒っている',
        script: {
          en: ['I hear you\'re frustrated about the delay.', 'I understand this is really important to you.', 'You need reliability and timely delivery.', 'Can we set up a weekly check-in to keep you updated?'],
          zh: ['我听到你对延迟感到不满。', '我理解这对你来说真的很重要。', '你需要的是可靠和及时的交付。', '我们可以建立每周沟通机制来跟进进度吗？'],
          ja: ['遅延についてお怒りの気持ちを聞いています。', 'これが本当に重要だと理解しています。', '信頼性とタイムリーな納品が必要ですよね。', '週次チェックインを設定して、進捗をお伝えしましょうか？'],
        },
      },
      {
        en: 'Client doubts accuracy', zh: '客户质疑准确性', ja: 'クライアントが正確性を疑っている',
        script: {
          en: ['What you described matches what I see in the data.', 'It\'s normal to be skeptical at first.', 'You need proof before committing.', 'Let me show you one specific detail — see if it resonates.'],
          zh: ['你说的情况和我看到的数据是一致的。', '一开始有怀疑是很正常的。', '你需要的是验证。', '让我给你看一个具体细节——看看是否吻合。'],
          ja: ['おっしゃったことはデータと一致しています。', '最初は疑うのは普通です。', '確証が必要ですよね。', '具体的な詳細をお見せします——合っているか確認してください。'],
        },
      },
      {
        en: 'Client faces big decision', zh: '客户面临重大抉择', ja: 'クライアントが大きな選択に直面',
        script: {
          en: ['You\'re at a crossroads with two strong options.', 'This kind of uncertainty is stressful.', 'You need clarity, not more opinions.', 'Let\'s map out the pros and cons of each path.'],
          zh: ['你正面临两个都不错的选择。', '这种不确定性确实让人压力大。', '你需要的是清晰的判断依据。', '让我们列出两条路的利弊。'],
          ja: ['二つの強い選択肢の交差点にいます。', 'この不確実さはストレスが大きいです。', '必要的是清晰さ、opinions ではありません。', 'それぞれの道の長所と短所を整理しましょう。'],
        },
      },
    ],
  },

  // ═══════════════════════════════════════════════
  // 鬼谷子 (Guiguzi)
  // ═══════════════════════════════════════════════
  guiguzi: {
    name: { en: 'Guiguzi Strategy', zh: '鬼谷子谋略', ja: '鬼谷子戦略' },
    period: 'Warring States (战国时期)',
    tactics: [
      { zh: '揣摩', en: 'Chuai Mo (Assess)', ja: '揣摩（かいま）', desc_en: 'Read the person — observe words, body language, context', desc_zh: '揣摩人心——观察言行、肢体语言、情境', desc_ja: '人物を読む——言葉、ボディーランクス、状況を観察' },
      { zh: '权谋', en: 'Quan Mou (Weigh)', ja: '権謀（けんぼう）', desc_en: 'Weigh options — present alternatives strategically', desc_zh: '权衡利弊——有策略地呈现选项', desc_ja: '選択肢を比較——戦略的に提示する' },
      { zh: '决策', en: 'Jue Ce (Decide)', ja: '決策（けっさく）', desc_en: 'Guide to decision — help them choose confidently', desc_zh: '引导决策——帮助他们自信地选择', desc_ja: '意思決定を導く——自信を選べるように' },
      { zh: '捭阖', en: 'Bai He (Open/Close)', ja: '捭阖（はいこう）', desc_en: 'Control flow — open conversation, then close with ask', desc_zh: '捭阖之道——打开话题，然后收束到请求', desc_ja: '流れを制御——会話を開き、要求で閉じる' },
    ],
    scenarios: [
      {
        en: 'Negotiation understanding', zh: '谈判中的理解', ja: '交渉における理解',
        script: {
          en: ['I sense there\'s something beyond the price you\'re weighing.', 'Your tone shifts when you mention the timeline — that matters more.', 'You need a partner, not just a vendor.', 'What if we explored what \'right fit\' means to you?'],
          zh: ['我感觉到你在价格之外还有其他顾虑。', '你提到时间线时语气变了——那对你更重要。', '你需要的是合作伙伴，而不仅仅是供应商。', '如果我们一起探讨"合适的合作"对你意味着什么？'],
          ja: ['価格以外にweightingされている何かがあると感じます。', 'タイムラインに言及した時、口調が変わります——それが重要ですよね。', 'パートナーとしての関係が必要です。', '「適切な適合」がどのような意味か、一緒に探ってみませんか？'],
        },
      },
      {
        en: 'Persuasion through empathy', zh: '通过共情进行说服', ja: '共感を通じた説得',
        script: {
          en: ['I can see this direction would create risk for your team.', 'The hesitation makes sense given past experience.', 'You need confidence that this won\'t repeat old mistakes.', 'Let me share how we specifically addressed those past failures.', 'Then you can decide if this feels different.'],
          zh: ['我能看到这个方向会给你的团队带来风险。', '根据过去的经验，犹豫是完全合理的。', '你需要的是信心——确保这不会重蹈覆辙。', '让我分享我们如何具体解决过去的那些问题。', '然后你可以判断这次是否不同。'],
          ja: ['この方向がチームにとってリスクになると理解しています。', '過去の経験からためらうのは当然です。', '同じ失敗を繰り返さないという確信が必要ですね。', '過去の問題をどのように具体的に解決したか、共有させてください。', 'その後、今回はどう違うか判断してみてください。'],
        },
      },
      {
        en: 'Reading the room', zh: '洞察现场氛围', ja: '場の空気を読む',
        script: {
          en: ['I notice the energy shifted when we discussed scope.', 'There might be concerns not yet spoken aloud.', 'Creating space for honesty helps everyone.', 'What would make this feel safe enough to discuss openly?'],
          zh: ['我注意到讨论范围时，现场的气氛变了。', '可能有一些顾虑还没有被说出来。', '营造坦诚的氛围对所有人都有益。', '怎样的方式能让大家觉得安全到愿意公开讨论？'],
          ja: ['範囲について議論した時、空気が変わったと感じました。', 'まだ口にされていない懸念があるかもしれません。', '率直さを許す空間を作ることは全員にとって良いことです。', '率直に話し合えるような安全な雰囲気を作るにはどうしたら良いですか？'],
        },
      },
    ],
  },

  // ═══════════════════════════════════════════════
  // 孙子兵法 (Sun Tzu)
  // ═══════════════════════════════════════════════
  sunzu: {
    name: { en: 'Sun Tzu Art of War', zh: '孙子兵法', ja: '孫子の兵法' },
    principles: [
      { zh: '知彼知己', en: 'Know Your Enemy', ja: '知彼知己', desc_en: 'Research client and competitor before pitching', desc_zh: '了解客户和竞品再做提案', desc_ja: '提案前にクライアントと競合を調査' },
      { zh: '以正合以奇胜', en: 'Strategy + Surprise', ja: '以正合以奇勝', desc_en: 'Combine logical approach with creative twist', desc_zh: '逻辑方法+创意转折', desc_ja: '論理的アプローチ+クリエイティブな展開' },
      { zh: '投之亡地然后存', en: 'Situational Awareness', ja: '死地に投じて存する', desc_en: 'Understand pressure dynamics — recognize urgency vs manufactured pressure', desc_zh: '理解压力动态——辨别真实紧迫感和人为压力', desc_ja: 'プレッシャーの動態を理解——切迫感が真か捏造かを識別' },
      { zh: '上兵伐谋', en: 'Win Without Fighting', ja: '上兵は謀を伐つ', desc_en: 'Win through strategy, not confrontation', desc_zh: '用策略取胜，而非对抗', desc_ja: '対立せずに戦略で勝つ' },
    ],
    scenarios: [
      {
        en: 'Competitive landscape', zh: '竞争格局分析', ja: '競争環境の分析',
        script: {
          en: ['Before we pitch, let\'s map what they already know about alternatives.', 'Understanding their current satisfaction tells us where the gaps are.', 'We position not against them, but alongside their unmet needs.', 'The strongest pitch shows you\'ve done your homework.', 'Let them feel understood, not sold to.'],
          zh: ['在提案之前，先了解他们对替代方案的认知。', '了解他们当前的满意程度，能帮我们找到缺口。', '我们的定位不是对抗他们，而是契合他们未被满足的需求。', '最强的提案是让他们感受到你做了功课。', '让他们感到被理解，而不是被推销。'],
          ja: ['提案前に、代替案についてすでに知っていることを把握しましょう。', '現在の満足度を理解することで、ギャップが見えてきます。', '彼らに対してではなく、未充足のニーズに寄り添うポジショニングです。', '最も強い提案は、事前調査をしっかりしたことを感じさせること。', '売込みではなく、理解されたと感じさせてあげましょう。'],
        },
      },
      {
        en: 'Strategic positioning', zh: '战略性定位', ja: '戦略的ポジショニング',
        script: {
          en: ['Know what battle you\'re actually fighting — is it price, trust, or timing?', 'The terrain is their internal politics and decision process.', 'Win their hearts before their spreadsheets.', 'Sometimes the best strategy is patience and timing.'],
          zh: ['先弄清楚你实际在打的仗是什么——是价格、信任，还是时机？', '真正的地形是他们的内部政治和决策流程。', '先赢得他们的心，再赢他们的预算表。', '有时候最好的策略是耐心和时机。'],
          ja: ['本当に戦っているのは何かを把握する——価格か信頼かタイミングか？', '本当の地形は内部政治と意思決定プロセスです。', 'まず心を赢得てから、スプレッドシートを贏つ。', '時に最善の戦略は忍耐とタイミングです。'],
        },
      },
      {
        en: 'Reading competitive dynamics', zh: '洞察竞争动态', ja: '競争動向の理解',
        script: {
          en: ['What is the competitor not telling them? That\'s where opportunity lives.', 'Don\'t attack rivals — highlight your unique value quietly.', 'The client\'s biggest fear isn\'t choosing wrong; it\'s being uninformed.', 'Equip them with knowledge, and the right choice becomes obvious.', 'Let the facts speak louder than your words.'],
          zh: ['竞争对手没有告诉他们什么？那就是机会所在。', '不要攻击对手——安静地凸显你的独特价值。', '客户最大的恐惧不是选错，而是信息不足。', '给他们知识，正确的选择就会变得清晰。', '让事实比你的话语更有说服力。'],
          ja: ['競合は何を伝えられていないか？そこがチャンスです。', '競合を攻撃しない——独自の価値を静かに示しましょう。', 'クライアントの最大の恐怖は選択を間違えることではなく、情報不足です。', '知識を与えれば、正しい選択は自然と明らかになります。', '言葉よりも事実を語らせてください。'],
        },
      },
    ],
  },

  // ═══════════════════════════════════════════════
  // 西奥迪尼影响力 (Cialdini)
  // ═══════════════════════════════════════════════
  cialdini: {
    name: { en: 'Cialdini\'s Influence', zh: '西奥迪尼影响力原则', ja: 'チャルディーニの影響力' },
    principles: [
      { en: 'Reciprocity', zh: '互惠', ja: '互恵', desc_en: 'Give value first — they\'ll want to return the favor', desc_zh: '先给予价值——他们会想要回报', desc_ja: '先に価値を与える——お返ししたくなる' },
      { en: 'Commitment', zh: '承诺与一致', ja: 'コミットメント', desc_en: 'Small yes leads to big yes', desc_zh: '小的同意引导大的同意', desc_ja: '小さなYesが大きなYesにつながる' },
      { en: 'Social Proof', zh: '社会认同', ja: '社会的証明', desc_en: 'Show others have done it successfully', desc_zh: '展示其他人已经成功做过', desc_ja: '他の人が成功したことを示す' },
      { en: 'Authority', zh: '权威', ja: '権威', desc_en: 'Establish expertise and credibility', desc_zh: '建立专业性和可信度', desc_ja: '専門性と信頼性を確立する' },
      { en: 'Liking', zh: '喜好', ja: '好意', desc_en: 'Genuine rapport building — mutual respect', desc_zh: '真诚喜好——建立好感，相互尊重', desc_ja: '真の好意——好感を築き、相互尊重' },
      { en: 'Scarcity', zh: '稀缺', ja: '希少性', desc_en: 'Real limited availability — only reference genuine constraints', desc_zh: '真实有限的供应——只引用真实的限制条件', desc_ja: '真の限定数量——本当に制限がある場合のみ' },
    ],
    scenarios: [
      {
        en: 'Ethical influence in practice', zh: '伦理影响力的实践', ja: '倫理的影響力の実践',
        script: {
          en: ['I want to share something valuable with you — no strings attached.', 'If this helps, I\'d appreciate you keeping me in mind for future needs.', 'Here\'s what others in similar situations have experienced — their stories are public.', 'I share this not to pressure you, but because the expertise speaks for itself.', 'I genuinely enjoy working with people who value quality — and I can tell you do.', 'This specific configuration is genuinely limited because of the specialist team required.'],
          zh: ['我想先分享一些有价值的东西——没有任何附加条件。', '如果这对你有帮助，希望未来有需要时你能想到我。', '以下是类似情况的人的经历——他们的故事是公开的。', '我分享这些不是要给你压力，而是因为专业能力本身就说明了一切。', '我真心喜欢和重视质量的人合作——我看得出你是这样的人。', '这个特定配置确实是有限的，因为需要专业团队支持。'],
          ja: ['まず価値のある共有をさせてください——見返りは一切不要です。', 'これが役に立てば、今後のご相談でまたご連絡いただければ嬉しいです。', '同様の状況の方々の体験を共有します——すべて公表済みです。', 'プレッシャーをかけるためではなく、専門性が物語っているから共有します。', '質を重んじる方々とのお仕事を本当に Enjoy しています——あなたがまさにその方だと感じています。', 'この特定の構成は、必要な専門チームのため、本当に限定的です。'],
        },
      },
      {
        en: 'Building genuine trust', zh: '建立真诚的信任', ja: '真の信頼を築く',
        script: {
          en: ['I\'d rather lose this deal than compromise your trust.', 'Let me be transparent about what we can and cannot do.', 'I\'ll connect you with a client who had concerns just like yours.', 'The best partnerships start with honesty, not promises.'],
          zh: ['我宁愿失去这笔交易，也不愿损害你的信任。', '让我坦诚告诉你我们能做什么、不能做什么。', '我帮你对接一个曾有和你同样顾虑的客户。', '最好的合作关系始于诚实，而非承诺。'],
          ja: ['この取引を失う方が、あなたの信頼を損なうよりましです。', 'できることとできないことを正直にお伝えします。', 'あなたと同じ懸念をお持ちだったクライアントをご紹介します。', '最高のパートナーシップは約束ではなく誠実さから始まります。'],
        },
      },
      {
        en: 'Overcoming objections with respect', zh: '尊重地回应异议', ja: '敬意を持って異議に対応する',
        script: {
          en: ['That\'s a valid concern — let me address it directly.', 'I understand why you\'d feel that way based on your experience.', 'Here\'s what I can offer, and here\'s what I honestly cannot.', 'Would it help to see how this has worked for others in your exact situation?', 'There\'s no rush — take the time you need to feel confident.'],
          zh: ['这是一个合理的顾虑——让我直接回应。', '根据你的经历，我理解你为什么会有这种感受。', '以下是我能提供的，以及我坦诚做不到的。', '如果看看和你情况完全一样的人如何成功的案例，会有帮助吗？', '不着急——花你需要的时间去建立信心。'],
          ja: ['その懸念は正当です——直接お答えします。', 'あなたの経験から、なぜそう感じるのか理解できます。', '以下が提供できること、そして正直にお伝えできないことです。', '全く同じ状況の方々がどのように成功したか見てみるのはいかがですか？', '急ぐ必要はありません——自信を持てるまで十分にお時間を使ってください。'],
        },
      },
    ],
  },

  // ═══════════════════════════════════════════════
  // 认知偏差 (Cognitive Biases)
  // ═══════════════════════════════════════════════
  biases: {
    name: { en: 'Cognitive Bias Awareness', zh: '认知偏差觉察', ja: '認知バイアスの気づき' },
    items: [
      { en: 'Anchoring', zh: '锚定效应', ja: 'アンカリング', desc_en: 'How initial numbers shape perception — recognize when it happens to you', desc_zh: '初始数字如何影响判断——觉察自己何时被锚定', desc_ja: '最初の数字が認識をどう形作るか——自分に起こるときを察知' },
      { en: 'Loss Aversion', zh: '损失厌恶', ja: '損失回避', desc_en: 'Losses feel 2x stronger than gains — be aware of fear-driven decisions', desc_zh: '损失的感受是收益的2倍——警惕恐惧驱动的决策', desc_ja: '損失の感受は利益の2倍——恐怖に驱动される意思決定に注意' },
      { en: 'Bandwagon', zh: '从众效应', ja: 'バンドワゴン効果', desc_en: 'We follow the crowd — question whether the crowd is right', desc_zh: '我们倾向于跟随大众——质疑大众是否正确', desc_ja: '私たちは衆に従う——衆が正しいか疑う' },
      { en: 'IKEA Effect', zh: '宜家效应', ja: 'IKEA効果', desc_en: 'We overvalue what we build — notice attachment bias', desc_zh: '我们高估自己参与创造的东西——注意禀赋效应', desc_ja: '自分で作ったものを高く評価する——所有バイアスに注意' },
    ],
    scenarios: [
      {
        en: 'Recognizing manipulation', zh: '识别操纵行为', ja: '操作の識別',
        script: {
          en: ['They anchored high to make the real price feel reasonable.', 'The \'everyone\'s doing it\' claim needs verification, not assumption.', 'Am I being influenced by urgency, or by genuine need?', 'Let me separate the emotional pull from the factual basis.', 'Ask: would I choose this if nobody else were watching?'],
          zh: ['他们先报高价，让真实价格显得合理。', '"所有人都在这样做"的说法需要验证，不能想当然。', '我是被紧迫感影响，还是出于真实需求？', '让我把情绪驱动和事实依据分开。', '问问自己：如果没人在看，我还会选择这个吗？'],
          ja: ['相手は高い数字を先に出し、本物の価格が妥当に見えるようにしています。', '「みんなやっている」という主張は、仮定ではなく検証が必要です。', '切迫感に影響されているのか、それとも本物のニーズなのか？', '感情の引きと事実の根拠を分けて考えましょう。', '问他：誰も見ていなければ、それでもこの選択をするか？'],
        },
      },
      {
        en: 'Informed decision-making', zh: '知情决策', ja: '情報に基づいた意思決定',
        script: {
          en: ['What number am I anchored to, and is it realistic?', 'Is the \'limited time\' pressure real, or manufactured?', 'Am I following the crowd, or have I done my own analysis?', 'Do I value this because it\'s good, or because I built it?', 'Write down your decision criteria before hearing the pitch.'],
          zh: ['我被锚定在什么数字上，这现实吗？', '"限时"的压力是真的，还是人为制造的？', '我是在跟随大众，还是做了自己的分析？', '我重视它是因为它真的好，还是因为我参与了？', '在听到推销之前，先写下你的决策标准。'],
          ja: ['私はどの数字にアンカリングされているか、それは現実的か？', '「期間限定」のプレッシャーは本物か、それとも作られたものか？', 'みんなに従っているのか、それとも自分で分析したのか？', '良いから評価しているのか、自分が作ったから評価しているのか？', '提案を聞く前に、意思決定基準を書き出しましょう。'],
        },
      },
      {
        en: 'Self-awareness check', zh: '自我觉察检查', ja: '自己認識チェック',
        script: {
          en: ['I notice I\'m drawn to this because others want it too.', 'The fear of missing out is real, but is the opportunity real?', 'My emotional reaction might be a signal — or a vulnerability.', 'What would a complete outsider advise me to do?', 'Pause. Breathe. Then decide with clear eyes.'],
          zh: ['我注意到我被这个吸引，是因为别人也想要它。', '错过的恐惧是真实的，但机会是真实的吗？', '我的情绪反应可能是一个信号——也可能是一个弱点。', '一个完全的局外人会建议我怎么做？', '暂停。呼吸。然后用清醒的头脑做决定。'],
          ja: ['他の人も欲しがっているから惹かれていると気づきました。', '見逃す恐怖は本物ですが、チャンスは本物か？', '感情的な反応はシグナルかもしれません——あるいは弱点かもしれません。', '完全な外部者ならどう助言するか？', '一呼吸置いてください。深呼吸。そして冷静に判断しましょう。'],
        },
      },
    ],
  },
};

module.exports = frameworks;
