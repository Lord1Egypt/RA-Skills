/**
 * High-EQ Communication i18n (11 Languages)
 * 高情商沟通多语言数据
 * 
 * Languages: en, zh, ja, ko, ms, hi, ar, es, de, fr, it
 */

const i18n = {
  // ═══════════════════════════════════════════════
  // UI Labels
  // ═══════════════════════════════════════════════
  labels: {
    en: { title:'High-EQ Communication Toolkit', framework:'Framework', scenario:'Scenario', principle:'Principle', steps:'Steps', script:'Script', when:'When to Use', desc:'Description', sources:'Sources', observation:'Observation', feeling:'Feeling', need:'Need', request:'Request', tactics:'Tactics', items:'Items' },
    zh: { title:'高情商沟通工具包', framework:'框架', scenario:'场景', principle:'原则', steps:'步骤', script:'话术', when:'适用场景', desc:'说明', sources:'知识来源', observation:'观察', feeling:'感受', need:'需要', request:'请求', tactics:'策略', items:'条目' },
    ja: { title:'高EQコミュニケーションツールキット', framework:'フレームワーク', scenario:'シナリオ', principle:'原則', steps:'ステップ', script:'スクリプト', when:'使用場面', desc:'説明', sources:'情報源', observation:'観察', feeling:'感情', need:'必要', request:'要求', tactics:'戦術', items:'項目' },
    ko: { title:'고EQ 커뮤니케이션 툴킷', framework:'프레임워크', scenario:'시나리오', principle:'원칙', steps:'단계', script:'스크립트', when:'사용 시점', desc:'설명', sources:'출처', observation:'관찰', feeling:'감정', need:'필요', request:'요청', tactics:'전술', items:'항목' },
    ms: { title:'Kit Komunikasi Ber-EQ Tinggi', framework:'Rangka Kerja', scenario:'Senario', principle:'Prinsip', steps:'Langkah', script:'Skrip', when:'Bila Digunakan', desc:'Penerangan', sources:'Sumber', observation:'Pemerhatian', feeling:'Perasaan', need:'Keperluan', request:'Permintaan', tactics:'Taktik', items:'Item' },
    hi: { title:'उच्च EQ संचार टूलकिट', framework:'फ्रेमवर्क', scenario:'परिदृश्य', principle:'सिद्धांत', steps:'चरण', script:'स्क्रिप्ट', when:'कब उपयोग करें', desc:'विवरण', sources:'स्रोत', observation:'अवलोकन', feeling:'भावना', need:'आवश्यकता', request:'अनुरोध', tactics:'रणनीति', items:'आइटम' },
    ar: { title:'أدوات التواصل العاطفي العالي', framework:'إطار عمل', scenario:'سيناريو', principle:'مبدأ', steps:'خطوات', script:'نص', when:'متى تُستخدم', desc:'وصف', sources:'مصادر', observation:'مراقبة', feeling:'شعور', need:'حاجة', request:'طلب', tactics:'تكتيكات', items:'عناصر' },
    es: { title:'Kit de Comunicación de Alto EQ', framework:'Marco', scenario:'Escenario', principle:'Principio', steps:'Pasos', script:'Guión', when:'Cuándo usar', desc:'Descripción', sources:'Fuentes', observation:'Observación', feeling:'Sentimiento', need:'Necesidad', request:'Solicitud', tactics:'Tácticas', items:'Elementos' },
    de: { title:'High-EQ Kommunikations-Toolkit', framework:'Rahmen', scenario:'Szenario', principle:'Prinzip', steps:'Schritte', script:'Skript', when:'Wann verwenden', desc:'Beschreibung', sources:'Quellen', observation:'Beobachtung', feeling:'Gefühl', need:'Bedürfnis', request:'Bitte', tactics:'Taktiken', items:'Elemente' },
    fr: { title:'Kit de Communication Haut EQ', framework:'Cadre', scenario:'Scénario', principle:'Principe', steps:'Étapes', script:'Script', when:'Quand utiliser', desc:'Description', sources:'Sources', observation:'Observation', feeling:'Sentiment', need:'Besoin', request:'Demande', tactics:'Tactiques', items:'Éléments' },
    it: { title:'Kit di Comunicazione Alto EQ', framework:'Cornice', scenario:'Scenario', principle:'Principio', steps:'Passi', script:'Script', when:'Quando usare', desc:'Descrizione', sources:'Fonti', observation:'Osservazione', feeling:'Sentimento', need:'Bisogno', request:'Richiesta', tactics:'Tattiche', items:'Elementi' },
  },

  // ═══════════════════════════════════════════════
  // NVC Steps
  // ═══════════════════════════════════════════════
  nvcSteps: {
    en: ['Observation (objective facts)', 'Feeling (emotional response)', 'Need (underlying desire)', 'Request (specific action)'],
    zh: ['观察（客观事实）', '感受（情绪反应）', '需要（深层需求）', '请求（具体行动）'],
    ja: ['観察（客観的事実）', '感情（感情的反応）', '必要（根底にある欲求）', '要求（具体的な行動）'],
    ko: ['관찰 (객관적 사실)', '감정 (정서적 반응)', '필요 (근본적 욕구)', '요청 (구체적 행동)'],
    ms: ['Pemerhatian (fakta objektif)', 'Perasaan (tindak balas emosi)', 'Keperluan (keinginan mendasar)', 'Permintaan (tindakan spesifik)'],
    hi: ['अवलोकन (वस्तुनिष्ठ तथ्य)', 'भावना (भावनात्मक प्रतिक्रिया)', 'आवश्यकता (अंतर्निहित इच्छा)', 'अनुरोध (विशिष्ट कार्य)'],
    ar: ['مراقبة (حقائق موضوعية)', 'شعور (استجابة عاطفية)', 'حاجة (رغبة أساسية)', 'طلب (إجراء محدد)'],
    es: ['Observación (hechos objetivos)', 'Sentimiento (respuesta emocional)', 'Necesidad (deseo subyacente)', 'Solicitud (acción específica)'],
    de: ['Beobachtung (objektive Fakten)', 'Gefühl (emotionale Reaktion)', 'Bedürfnis (zugrunde liegender Wunsch)', 'Bitte (spezifische Aktion)'],
    fr: ['Observation (faits objectifs)', 'Sentiment (réponse émotionnelle)', 'Besoin (désir sous-jacent)', 'Demande (action spécifique)'],
    it: ['Osservazione (fatti oggettivi)', 'Sentimento (risposta emotiva)', 'Bisogno (desiderio sottostante)', 'Richiesta (azione specifica)'],
  },

  // ═══════════════════════════════════════════════
  // NVC Scenarios
  // ═══════════════════════════════════════════════
  nvcScenarios: {
    angry: {
      en: { name:'Client is angry', script:['I hear you\'re frustrated about the delay.','I understand this is really important to you.','You need reliability and timely delivery.','Can we set up a weekly check-in to keep you updated?'] },
      zh: { name:'客户愤怒', script:['我听到你对延迟感到不满。','我理解这对你来说真的很重要。','你需要的是可靠和及时的交付。','我们可以建立每周沟通机制来跟进进度吗？'] },
      ja: { name:'クライアントが怒っている', script:['遅延についてお怒りの気持ちを聞いています。','これが本当に重要だと理解しています。','信頼性とタイムリーな納品が必要ですよね。','週次チェックインを設定して、進捗をお伝えしましょうか？'] },
      ko: { name:'고객이 화가 나있을 때', script:['지연에 대해 좌절하고 계시다는 것을 듣습니다.','이것이 정말 중요하다는 것을 이해합니다.','신뢰성과 적시 납품이 필요하시죠.','주간 체크인을 설정해서 진행 상황을 알려드릴까요?'] },
      ms: { name:'Pelanggan marah', script:['Saya dengar anda kecewa dengan kelewahan.','Saya faham ini sangat penting untuk anda.','Anda perlukan kebolehpercayaan dan penghantaran tepat masa.','Boleh kita tetapkan semakan mingguan untuk maklumkan perkembangan?'] },
      hi: { name:'ग्राहक नाराज़ है', script:['मैं सुन रहा हूँ कि आप देरी से निराश हैं।','मैं समझता हूँ कि यह वास्तव में आपके लिए महत्वपूर्ण है।','आपको विश्वसनीयता और समय पर डिलीवरी चाहिए।','क्या हम साप्ताहिक जांच स्थापित कर सकते हैं?'] },
      ar: { name:'العميل غاضب', script:['أسمع أنك محبط من التأخير.','أفهم أن هذا مهم جداً لك.','أنت تحتاج موثوقية وتسليم في الوقت.','هل يمكننا إعداد متابعة أسبوعية لإبقائك على اطلاع؟'] },
      es: { name:'Cliente está enojado', script:['Escucho que estás frustrado por el retraso.','Entiendo que esto es muy importante para ti.','Necesitas confiabilidad y entrega puntual.','¿Podemos establecer un seguimiento semanal?'] },
      de: { name:'Klient ist wütend', script:['Ich höre, dass Sie über die Verzögerung frustriert sind.','Ich verstehe, dass Ihnen das wirklich wichtig ist.','Sie brauchen Zuverlässigkeit und termingerechte Lieferung.','Können wir ein wöchentliches Check-in einrichten?'] },
      fr: { name:'Le client est en colère', script:['J\'entends que vous êtes frustré par le retard.','Je comprends que c\'est vraiment important pour vous.','Vous avez besoin de fiabilité et de livraison ponctuelle.','Pouvons-nous mettre en place un suivi hebdomadaire?'] },
      it: { name:'Il cliente è arrabbiato', script:['Sento che sei frustrato per il ritardo.','Capisco che questo è davvero importante per te.','Hai bisogno di affidabilità e consegna puntuale.','Possiamo impostare un check-in settimanale?'] },
    },
    doubt: {
      en: { name:'Client doubts accuracy', script:['What you described matches what I see in the data.','It\'s normal to be skeptical at first.','You need proof before committing.','Let me show you one specific detail — see if it resonates.'] },
      zh: { name:'客户质疑准确性', script:['你说的情况和我看到的数据是一致的。','一开始有怀疑是很正常的。','你需要的是验证。','让我给你看一个具体细节——看看是否吻合。'] },
      ja: { name:'クライアントが正確性を疑っている', script:['おっしゃったことはデータと一致しています。','最初は疑うのは普通です。','確証が必要ですよね。','具体的な詳細をお見せします——合っているか確認してください。'] },
      ko: { name:'고객이 정확성을 의심할 때', script:['말씀하신 내용이 데이터와 일치합니다.','처음에는 회의적인 것이 정상입니다.','증거가 필요하시죠.','구체적인 세부사항을 보여드릴게요 — 맞는지 확인해보세요.'] },
      ms: { name:'Pelanggan ragu', script:['Apa yang anda terangkan sepadan dengan data.','Normal untuk berwaspada pada mulanya.','Anda perlukan bukti sebelum komit.','Saya tunjukkan satu butiran — lihat jika ia resonates.'] },
      hi: { name:'ग्राहक को शक है', script:['जो आपने बताया वह डेटा से मेल खाता है।','शुरू में शंका होना सामान्य है।','आपको सबूत चाहिए।','मैं एक विशिष्ट विवरण दिखाता हूँ — देखें कि क्या यह सही है।'] },
      ar: { name:'العميل يشك في الدقة', script:['ما وصفته يتطابق مع ما أراه في البيانات.','من الطبيعي أن تكون متشككاً في البداية.','أنت تحتاج دليلاً قبل الالتزام.','دعني أُريك تفصيلاً محدداً — انظر إذا كان يتردد.'] },
      es: { name:'Cliente duda de la exactitud', script:['Lo que describes coincide con los datos.','Es normal ser escéptico al principio.','Necesitas pruebas antes de comprometerte.','Déjame mostrarte un detalle específico.'] },
      de: { name:'Klient zweifelt an Genauigkeit', script:['Das, was Sie beschreiben, stimmt mit den Daten überein.','Es ist normal, anfangs skeptisch zu sein.','Sie brauchen Beweise vor der Zusage.','Lassen Sie mich ein Detail zeigen — sehen Sie, ob es passt.'] },
      fr: { name:'Le client doute de la précision', script:['Ce que vous décrivez correspond aux données.','Il est normal d\'être sceptique au début.','Vous avez besoin de preuves avant de vous engager.','Laissez-moi vous montrer un détail spécifique.'] },
      it: { name:'Il cliente dubita della precisione', script:['Quello che descrivi corrisponde ai dati.','È normale essere scettici all\'inizio.','Hai bisogno di prove prima di impegnarti.','Lasciame mostrare un dettaglio specifico.'] },
    },
    decision: {
      en: { name:'Client faces big decision', script:['You\'re at a crossroads with two strong options.','This kind of uncertainty is stressful.','You need clarity, not more opinions.','Let\'s map out the pros and cons of each path.'] },
      zh: { name:'客户面临重大抉择', script:['你正面临两个都不错的选择。','这种不确定性确实让人压力大。','你需要的是清晰的判断依据。','让我们列出两条路的利弊。'] },
      ja: { name:'クライアントが大きな選択に直面', script:['二つの強い選択肢の交差点にいます。','この不確実さはストレスが大きいです。','必要的是清晰さ、意见ではありません。','それぞれの道の長所と短所を整理しましょう。'] },
      ko: { name:'고객이 큰 결정에 직면', script:['두 가지 강력한 선택지가 있는 교차점에 있습니다.','이런 불확실성은 스트레스가 큽니다.','명확함이 필요하시지, 더 많은 의견이 아닙니다.','각 경로의 장단점을 정리해봅시다.'] },
      ms: { name:'Pelanggan menghadapi keputusan besar', script:['Anda di persimpangan dengan dua pilihan.','Ketidakpastian ini memberi tekanan.','Anda perlukan kejelasan, bukan lebih banyak pendapat.','Mari kita senaraikan kelebihan dan kekurangan setiap laluan.'] },
      hi: { name:'ग्राहक बड़े फैसले के सामने', script:['आप दो मजबूत विकल्पों के चौराहे पर हैं।','इस तरह की अनिश्चितता तनावपूर्ण है।','आपको स्पष्टता चाहिए, और राय नहीं।','आइए प्रत्येक रास्ते के फायदे और नुकसान निकालें।'] },
      ar: { name:'العميل يواجه قراراً كبيراً', script:['أنت عند تقاطع طريقين قويين.','هذا النوع من عدم اليقين مرهق.','أنت تحتاج وضوحاً، ليستشارات أكثر.','دعنا نحدد إيجابيات وسلبيات كل مسار.'] },
      es: { name:'Cliente enfrenta gran decisión', script:['Estás en una encrucijada con dos opciones fuertes.','Esta incertidumbre es estresante.','Necesitas claridad, no más opiniones.','Repasemos los pros y contras de cada camino.'] },
      de: { name:'Klient steht vor großer Entscheidung', script:['Sie stehen an einem Kreuzweg mit zwei starken Optionen.','Diese Unsicherheit ist belastend.','Sie brauchen Klarheit, nicht mehr Meinungen.','Lassen wir uns die Vor- und Nachteile jedes Weges ansehen.'] },
      fr: { name:'Le client fait face à un grand choix', script:['Vous êtes à une croisée avec deux fortes options.','Cette incertitude est stressante.','Vous avez besoin de clarté, pas de plus d\'avis.','Définissons les avantages et inconvénients de chaque chemin.'] },
      it: { name:'Il cliente affronta una grande decisione', script:['Sei a un bivio con due forti opzioni.','Questa incertezza è stressante.','Hai bisogno di chiarezza, non di più pareri.','Definiamo pro e contro di ogni percorso.'] },
    },
  },

  // ═══════════════════════════════════════════════
  // Guiguzi Tactics
  // ═══════════════════════════════════════════════
  guiguziTactics: {
    en: [{ zh:'Chuai Mo',en:'Assess & Empathize',desc:'Read the person — observe words, body language, context' },{ zh:'Quan Mou',en:'Weigh Options',desc:'Present alternatives strategically' },{ zh:'Jue Ce',en:'Guide Decision',desc:'Help them choose confidently' },{ zh:'Bai He',en:'Open & Close',desc:'Control conversation flow' }],
    zh: [{ zh:'揣摩',en:'Chuai Mo',desc:'揣摩人心——观察言行、肢体语言、情境' },{ zh:'权谋',en:'Quan Mou',desc:'权衡利弊——有策略地呈现选项' },{ zh:'决策',en:'Jue Ce',desc:'引导决策——帮助他们自信地选择' },{ zh:'捭阖',en:'Bai He',desc:'捭阖之道——打开话题，然后收束到请求' }],
    ja: [{ zh:'揣摩',en:'Chuai Mo',desc:'人物を読む——言葉、ボディーランクス、状況を観察' },{ zh:'権謀',en:'Quan Mou',desc:'選択肢を比較——戦略的に提示する' },{ zh:'決策',en:'Jue Ce',desc:'意思決定を導く——自信を選べるように' },{ zh:'捭闔',en:'Bai He',desc:'流れを制御——会話を開き、要求で閉じる' }],
    ko: [{ zh:'Chuai Mo',en:'평가와 공감',desc:'상대를 읽기 — 말, 몸짓, 맥락 관찰' },{ zh:'Quan Mou',en:'옵션 비교',desc:'전략적으로 대안 제시' },{ zh:'Jue Ce',en:'결정 도움',desc:'자신 있게 선택하도록 돕기' },{ zh:'Bai He',en:'개폐',desc:'대화 흐름 제어' }],
    ms: [{ zh:'Chuai Mo',en:'Menilai & Berempati',desc:'Baca orang — perhatikan kata, bahasa badan, konteks' },{ zh:'Quan Mou',en:'Menimbang Pilihan',desc:'Sederhanakan alternatif secara strategik' },{ zh:'Jue Ce',en:'Membimbing Keputusan',desc:'Bantu mereka memilih dengan yakin' },{ zh:'Bai He',en:'Buka & Tutup',desc:'Kawal aliran percakapan' }],
    hi: [{ zh:'Chuai Mo',en:'आकलन और सहानुभूति',desc:'व्यक्ति को पढ़ें — शब्द, शारीरिक भाषा, संदर्भ देखें' },{ zh:'Quan Mou',en:'विकल्प तौलना',desc:'वैकल्पिक रूप से रणनीतिक रूप से प्रस्तुत करें' },{ zh:'Jue Ce',en:'निर्णय में मार्गदर्शन',desc:'उन्हें आत्मविश्वास से चुनने में मदद करें' },{ zh:'Bai He',en:'खोलें और बंद करें',desc:'बातचीत का प्रवाह नियंत्रित करें' }],
    ar: [{ zh:'Chuai Mo',en:'التقدير والتعاطف',desc:'اقرأ الشخص — راقب الكلمات ولغة الجسد والسياق' },{ zh:'Quan Mou',en:'وزن الخيارات',desc:'اعرض البدائل بشكل استراتيجي' },{ zh:'Jue Ce',en:'إرشاد القرار',desc:'ساعدهم على الاختيار بثقة' },{ zh:'Bai He',en:'فتح وإغلاق',desc:'تحكم في تدفق المحادثة' }],
    es: [{ zh:'Chuai Mo',en:'Evaluar y Empatizar',desc:'Leer a la persona — observar palabras, lenguaje corporal, contexto' },{ zh:'Quan Mou',en:'Ponderar Opciones',desc:'Presentar alternativas estratégicamente' },{ zh:'Jue Ce',en:'Guiar la Decisión',desc:'Ayudarles a elegir con confianza' },{ zh:'Bai He',en:'Abrir y Cerrar',desc:'Controlar el flujo de la conversación' }],
    de: [{ zh:'Chuai Mo',en:'Einschätzen & Einfühlen',desc:'Die Person lesen — Worte, Körpersprache, Kontext beobachten' },{ zh:'Quan Mou',en:'Optionen Abwägen',desc:'Alternativen strategisch präsentieren' },{ zh:'Jue Ce',en:'Entscheidung Leiten',desc:'Ihnen helfen, selbstbewusst zu wählen' },{ zh:'Bai He',en:'Öffnen & Schließen',desc:'Gesprächsfluss kontrollieren' }],
    fr: [{ zh:'Chuai Mo',en:'Évaluer et Empathiser',desc:'Lire la personne — observer les mots, le langage corporel, le contexte' },{ zh:'Quan Mou',en:'Peser les Options',desc:'Présenter les alternatives stratégiquement' },{ zh:'Jue Ce',en:'Guider la Décision',desc:'Les aider à choisir en confiance' },{ zh:'Bai He',en:'Ouvrir et Fermer',desc:'Contrôler le flux de la conversation' }],
    it: [{ zh:'Chuai Mo',en:'Valutare ed Empatizzare',desc:'Leggere la persona — osservare parole, linguaggio del corpo, contesto' },{ zh:'Quan Mou',en:'Pesare le Opzioni',desc:'Presentare le alternative strategicamente' },{ zh:'Jue Ce',en:'Guidare la Decisione',desc:'Aiutarli a scegliere con sicurezza' },{ zh:'Bai He',en:'Aprire e Chiudere',desc:'Controllare il flusso della conversazione' }],
  },

  // ═══════════════════════════════════════════════
  // Sun Tzu Principles
  // ═══════════════════════════════════════════════
  sunzuPrinciples: {
    en: [{ zh:'Know Yourself & Enemy',en:'Know yourself and your competitor',desc:'Research client and competitor before engaging' },{ zh:'Strategy + Surprise',en:'Win with strategy and creativity',desc:'Combine logical approach with creative twist' },{ zh:'Situational Awareness',en:'Understand pressure dynamics',desc:'Recognize urgency vs manufactured pressure' },{ zh:'Win Without Fighting',en:'Win through strategy, not confrontation',desc:'Use understanding, not argument' }],
    zh: [{ zh:'知彼知己',en:'Know Yourself & Enemy',desc:'了解客户和竞品再做沟通' },{ zh:'以正合以奇胜',en:'Strategy + Surprise',desc:'逻辑方法+创意转折' },{ zh:'投之亡地然后存',en:'Situational Awareness',desc:'理解压力动态——辨别真实紧迫感和人为压力' },{ zh:'上兵伐谋',en:'Win Without Fighting',desc:'用理解取胜，而非对抗' }],
    ja: [{ zh:'知彼知己',en:'Know Yourself & Enemy',desc:'提案前にクライアントと競合を調査' },{ zh:'以正合以奇勝',en:'Strategy + Surprise',desc:'論理的アプローチ+クリエイティブな展開' },{ zh:'死地に投じて存する',en:'Situational Awareness',desc:'プレッシャーの動態を理解——切迫感が真か捏造かを識別' },{ zh:'上兵は謀を伐つ',en:'Win Without Fighting',desc:'対立せずに理解で勝つ' }],
    ko: [{ zh:'지피지기',en:'Know Yourself & Enemy',desc:'상대와 경쟁사를 먼저 파악하라' },{ zh:'이정합이기승',en:'Strategy + Surprise',desc:'논리적 접근+창의적 전환' },{ zh:'지지에 투지하고연존',en:'Situational Awareness',desc:'압박의 역학을 이해 — 진짜 긴박함 vs 인위적 압력' },{ zh:'상병벌모',en:'Win Without Fighting',desc:'대립이 아닌 이해로 승리' }],
    ms: [{ zh:'Zhi Bi Zhi Ji',en:'Kenali Diri & Musuh',desc:'Kaji pelanggan dan pesaing sebelum berunding' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'Strategi + Kejutan',desc:'Gabung pendekatan logik dengan keunikan kreatif' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'Kesedaran Situasi',desc:'Fahami dinamik tekanan — bezakan tekanan sebenar vs buatan' },{ zh:'Shang Bing Fa Mou',en:'Menang Tanpa Bertelingkah',desc:'Menang melalui strategi, bukan konfrontasi' }],
    hi: [{ zh:'Zhi Bi Zhi Ji',en:'अपने आप और शत्रु को जानें',desc:'पिच से पहले ग्राहक और प्रतिस्पर्धी का अनुसंधान करें' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'रणनीति + आश्चर्य',desc:'तार्किक दृष्टिकोण + रचनात्मक मोड़ का संयोजन' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'स्थितिजन्य जागरूकता',desc:'दबाव की गतिशीलता को समझें' },{ zh:'Shang Bing Fa Mou',en:'बिना लड़ाई के जीतें',desc:'तर्क नहीं, समझ से जीतें' }],
    ar: [{ zh:'Zhi Bi Zhi Ji',en:'اعرف نفسك واعرف عدوك',desc:'ابحث عن العميل والمنافس قبل العرض' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'استراتيجية + مفاجأة',desc:'ادمج المنطق مع الإبداع' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'الوعي بالموقف',desc:'افهم ديناميكيات الضغط' },{ zh:'Shang Bing Fa Mou',en:'اربح بدون قتال',desc:'افهم بدل أن تجادل' }],
    es: [{ zh:'Zhi Bi Zhi Ji',en:'Conócete a ti y a tu rival',desc:'Investiga al cliente y competidor antes de presentar' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'Estrategia + Sorpresa',desc:'Combina enfoque lógico con creatividad' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'Conciencia Situacional',desc:'Entiende la dinámica de presión' },{ zh:'Shang Bing Fa Mou',en:'Gana sin confrontar',desc:'Gana con entendimiento, no con argumentos' }],
    de: [{ zh:'Zhi Bi Zhi Ji',en:'Kenne dich selbst und deinen Gegner',desc:'Recherche vor dem Pitch' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'Strategie + Überraschung',desc:'Logik + Kreativität kombinieren' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'Situationsbewusstsein',desc:'Druckdynamiken verstehen' },{ zh:'Shang Bing Fa Mou',en:'Gewinnen ohne Kampf',desc:'Durch Verständnis gewinnen, nicht durch Konfrontation' }],
    fr: [{ zh:'Zhi Bi Zhi Ji',en:'Connais-toi toi-même et ton rival',desc:'Recherche avant de pitcher' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'Stratégie + Surprise',desc:'Combiner logique et créativité' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'Conscience Situationnelle',desc:'Comprendre la dynamique de pression' },{ zh:'Shang Bing Fa Mou',en:'Gagner sans affronter',desc:'Gagner par la compréhension, pas par l\'argumentation' }],
    it: [{ zh:'Zhi Bi Zhi Ji',en:'Conosci te stesso e il tuo avversario',desc:'Ricerca prima del pitch' },{ zh:'Yi Zheng He Yi Qi Sheng',en:'Strategia + Sorpresa',desc:'Combina approccio logico e creatività' },{ zh:'Tou Zhi Wang Di Ran Hou Cun',en:'Consapevolezza Situazionale',desc:'Comprendere la dinamica della pressione' },{ zh:'Shang Bing Fa Mou',en:'Vincere senza combattere',desc:'Vincere con comprensione, non con confronto' }],
  },

  // ═══════════════════════════════════════════════
  // Cialdini Principles
  // ═══════════════════════════════════════════════
  cialdiniPrinciples: {
    en: [{ en:'Reciprocity',desc:'Genuine give-first mindset — they\'ll want to return the favor' },{ en:'Commitment',desc:'Consistency through small agreements' },{ en:'Social Proof',desc:'Authentic testimonials — show real success' },{ en:'Authority',desc:'Demonstrated expertise and credibility' },{ en:'Liking',desc:'Genuine rapport building — mutual respect' },{ en:'Scarcity',desc:'Real limited availability — only reference genuine constraints' }],
    zh: [{ zh:'互惠',desc:'真诚互惠——先给予价值，他们会想要回报' },{ zh:'承诺与一致',desc:'一致性承诺——小的同意引导大的同意' },{ zh:'社会认同',desc:'真实社会认同——展示其他人已经成功做过' },{ zh:'权威',desc:'实证权威——建立专业性和可信度' },{ zh:'喜好',desc:'真诚喜好——建立好感，相互尊重' },{ zh:'稀缺',desc:'真实稀缺——只引用真实的限制条件' }],
    ja: [{ zh:'互恵',desc:'真の互恵——先に価値を与えるとお返ししたくなる' },{ zh:'コミットメント',desc:'一貫性コミットメント——小さなYesが大きなYesにつながる' },{ zh:'社会的証明',desc:'真の社会的証明——他の人の成功した実例を示す' },{ zh:'権威',desc:'実証された権威——専門性と信頼性を確立する' },{ zh:'好意',desc:'真の好意——好感を築き、相互尊重' },{ zh:'希少性',desc:'真の希少性——本当に制限がある場合のみ' }],
    ko: [{ zh:'상호호혜',desc:'진정한 먼저 주는 마음 — 상대가 보답하고 싶어진다' },{ zh:'헌신과 일관성',desc:'작은 동의가 큰 동의로 이어진다' },{ zh:'사회적 증명',desc:'진정한 사례 — 실제 성공담을 보여준다' },{ zh:'권위',desc:'입증된 전문성과 신뢰성' },{ zh:'호감',desc:'진정한 관계 구축 — 상호 존중' },{ zh:'희소성',desc:'진정한 제한된 가용성 — 실제 제약만 언급' }],
    ms: [{ zh:'Timbal Balik',desc:'Sikap memberi dahulu yang tulus — mereka akan ingin membalas' },{ zh:'Komitmen',desc:'Konsistensi melalui perjanjian kecil' },{ zh:'Bukti Sosial',desc:'Testimoni autentik — tunjukkan kejayaan sebenar' },{ zh:'Otoriti',desc:' kepakaran dan kredibiliti yang terbukti' },{ zh:'Kegemaran',desc:'Membina hubungan yang tulus — rasa hormat timbal balik' },{ zh:'Kekurangan',desc:'Ketersediaan terhad yang nyata — hanya rujukan kendala sebenar' }],
    hi: [{ zh:'Pratikriya',desc:'ईमानदार पहले देने की मानसिकता — वे लौटाना चाहेंगे' },{ zh:'Pratibaddhata',desc:'छोटे समझौतों से निरंतरता' },{ zh:'Samajik Praman',desc:'प्रामाणिक प्रशंसापत्र — वास्तविक सफलता दिखाएं' },{ zh:'Satta',desc:'प्रदर्शित विशेषज्ञता और विश्वसनीयता' },{ zh:'Priyata',desc:'ईमानदार संबंध निर्माण — पारस्परिक सम्मान' },{ zh:'Apurtata',desc:'वास्तविक सीमित उपलब्धता — केवल वास्तविक बाधाओं का संदर्भ' }],
    ar: [{ zh:'المعاملة بالمثل',desc:'عقلية الصدق في العطاء — سيرغبون في رد الجميل' },{ zh:'الالتزام',desc:'الاستمرارية من خلال الاتفاقيات الصغيرة' },{ zh:'الدليل الاجتماعي',desc:'شهادات حقيقية — أظهر النجاح الفعلي' },{ zh:'السلطة',desc:'خبرة وموثوقية مثبتة' },{ zh:'المودة',desc:'بناء علاقة حقيقية — احترام متبادل' },{ zh:'الندرة',desc:'توفر محدود حقيقي — اذكر القيود الحقيقية فقط' }],
    es: [{ zh:'Reciprocidad',desc:'Mentalidad genuina de dar primero — querrán corresponder' },{ zh:'Compromiso',desc:'Consistencia a través de pequeños acuerdos' },{ zh:'Prueba Social',desc:'Testimonios auténticos — muestra éxito real' },{ zh:'Autoridad',desc:'Experiencia y credibilidad demostradas' },{ zh:'Agrado',desc:'Construcción genuina de rapport — respeto mutuo' },{ zh:'Escasez',desc:'Disponibilidad limitada real — solo referenciar restricciones genuinas' }],
    de: [{ zh:'Reziprozität',desc:'Aufrichtige Geben-zuerst-Haltung — sie werden erwidern wollen' },{ zh:'Commitment',desc:'Konsistenz durch kleine Vereinbarungen' },{ zh:'Sozialer Beweis',desc:'Echte Erfahrungsberichte — echten Erfolg zeigen' },{ zh:'Autorität',desc:'Bewiesene Expertise und Glaubwürdigkeit' },{ zh:'Zuneigung',desc:'Echte Beziehungsaufbau — gegenseitiger Respekt' },{ zh:'Knappheit',desc:'Echte eingeschränkte Verfügbarkeit — nur echte Einschränkungen nennen' }],
    fr: [{ zh:'Réciprocité',desc:'État d\'esprit authentique de donner d\'abord — ils voudront rendre le geste' },{ zh:'Engagement',desc:'Cohérence à travers petits accords' },{ zh:'Preuve Sociale',desc:'Témoignages authentiques — montrer le succès réel' },{ zh:'Autorité',desc:'Expertise et crédibilité démontrées' },{ zh:'Sympathie',desc:'Construction authentique de relation — respect mutuel' },{ zh:'Rareté',desc:'Disponibilité limitée réelle — ne référencer que les contraintes réelles' }],
    it: [{ zh:'Reciprocità',desc:'Mentalità genuina del dare per primo — vorranno ricambiare' },{ zh:'Impegno',desc:'Coerenza attraverso piccoli accordi' },{ zh:'Prova Sociale',desc:'Testimonianze autentiche — mostra successo reale' },{ zh:'Autorità',desc:'Competenza e credibilità dimostrate' },{ zh:'Simpatia',desc:'Costruzione genuina del rapporto — rispetto reciproco' },{ zh:'Scarsità',desc:'Disponibilità limitata reale — riferirsi solo a vincoli genuini' }],
  },

  // ═══════════════════════════════════════════════
  // Cognitive Biases
  // ═══════════════════════════════════════════════
  biases: {
    en: [{ en:'Anchoring',desc:'How initial numbers shape perception — recognize when it happens to you' },{ en:'Loss Aversion',desc:'Losses feel 2x stronger than gains — be aware of fear-driven decisions' },{ en:'Bandwagon',desc:'We follow the crowd — question whether the crowd is right' },{ en:'IKEA Effect',desc:'We overvalue what we build — notice attachment bias' }],
    zh: [{ zh:'锚定效应',desc:'初始数字如何影响判断——觉察自己何时被锚定' },{ zh:'损失厌恶',desc:'损失的感受是收益的2倍——警惕恐惧驱动的决策' },{ zh:'从众效应',desc:'我们倾向于跟随大众——质疑大众是否正确' },{ zh:'宜家效应',desc:'我们高估自己参与创造的东西——注意禀赋效应' }],
    ja: [{ zh:'アンカリング',desc:'最初の数字が認識をどう形作るか——自分に起こるときを察知' },{ zh:'損失回避',desc:'損失の感受は利益の2倍——恐怖に驱动される意思決定に注意' },{ zh:'バンドワゴン効果',desc:'私たちは衆に従う——衆が正しいか疑う' },{ zh:'IKEA効果',desc:'自分で作ったものを高く評価する——所有バイアスに注意' }],
    ko: [{ zh:'앵커링',desc:'처음 숫자가 인식을 어떻게 형성하는지 — 자신에게 일어날 때를 인식' },{ zh:'손실 회피',desc:'손실은 이득보다 2배 강하게 느껴진다 — 두려움에 의한 결정 경계' },{ zh:'밴드웨건 효과',desc:'우리는 군중을 따른다 — 군중이 옳은지 의문을 품자' },{ zh:'IKEA 효과',desc:'우리는 만든 것을 과대평가한다 — 애착 편향을 알아차리자' }],
    ms: [{ zh:'Anchoring',desc:'Angka awal membentuk persepsi — kenali bila ia berlaku kepada anda' },{ zh:'Loss Aversion',desc:'Kerugian terasa 2x lebih kuat dari keuntungan — berhati-hati dengan keputusan berfear' },{ zh:'Bandwagon',desc:'Kita mengikut orang ramai — soal sama ada orang ramai betul' },{ zh:'IKEA Effect',desc:'Kita melebihkan nilai benda yang kita cipta — perhatikan bias kekangan' }],
    hi: [{ zh:'Anchoring',desc:'शुरुआती संख्या धारणा को कैसे आकार देती है — जब यह आपके साथ हो तब पहचानें' },{ zh:'Loss Aversion',desc:'हानि लाभ से 2 गुना मजबूत महसूस होती है — भय-चालित निर्णयों से सावधान' },{ zh:'Bandwagon',desc:'हम भीड़ का अनुसरण करते हैं — सवाल करें कि क्या भीड़ सही है' },{ zh:'IKEA Effect',desc:'हम जो बनाते हैं उसे अधिक मूल्य देते हैं — आसक्ति पूर्वाग्रह को नोटिस करें' }],
    ar: [{ zh:'التثبيت',desc:'الأرقام الأولى تشكل الإدراك — تعرّف متى يحدث لك' },{ zh:'كره الفقد',desc:'الخسائر تشعر بضعف القوة مقارنة بالمكاسب — انتبه للقرارات المدفوعة بالخوف' },{ zh:'الاتجاه العام',desc:'نتبع الحشد — تسأل ما إذا كان الحشد محقاً' },{ zh:'تأثير IKEA',desc:'نبالغ في تقدير ما نبنيه — لاحظ التحيز في الارتباط' }],
    es: [{ zh:'Anclaje',desc:'Los números iniciales moldean la percepción — reconoce cuando te sucede' },{ zh:'Aversión a la Pérdida',desc:'Las pérdidas se sienten 2x más fuerte que las ganancias — cuidado con decisiones por miedo' },{ zh:'Efecto Bandwagon',desc:'Seguimos a la multitud — cuestiona si la multitud tiene razón' },{ zh:'Efecto IKEA',desc:'Sobrevaloramos lo que construimos — nota el sesgo de apego' }],
    de: [{ zh:'Verankering',desc:'Erste Zahlen formen die Wahrnehmung — erkennen, wenn es Ihnen passiert' },{ zh:'Verlustaversion',desc:'Verluste fühlen sich 2x stärker an als Gewinne — vorsicht bei Angst-Entscheidungen' },{ zh:'Bandwagon-Effekt',desc:'Wir folgen der Menge — hinterfragen, ob die Menge recht hat' },{ zh:'IKEA-Effekt',desc:'Wir überschätzen, was wir bauen — Merk Bias bemerken' }],
    fr: [{ zh:'Ancrage',desc:'Les premiers chiffres façonnent la perception — reconnaissez quand cela vous arrive' },{ zh:'Aversion à la Perte',desc:'Les pertes sont ressenties 2x plus fortement que les gains — méfiez-vous des décisions par peur' },{ zh:'Effet Bandwagon',desc:'Nous suivons la foule — questionnez si la foule a raison' },{ zh:'Effet IKEA',desc:'Nous surévaluons ce que nous construisons — remarquez le biais d\'attachement' }],
    it: [{ zh:'Ancoraggio',desc:'I primi numeri modellano la percezione — riconosci quando accade a te' },{ zh:'Avversione alle Perdite',desc:'Le perdite si sentono 2x più forti dei guadagni — attenzione alle decisioni guidate dalla paura' },{ zh:'Effetto Bandwagon',desc:'Seguiamo la massa — chiediti se la massa ha ragione' },{ zh:'Effetto IKEA',desc:'Sovrastimiamo ciò che costruiamo — nota il bias dell\'attaccamento' }],
  },

  // ═══════════════════════════════════════════════
  // Guiguzi Scenarios
  // ═══════════════════════════════════════════════
  guiguziScenarios: {
    negotiate: {
      en: 'Negotiation Understanding', zh: '谈判中的理解', ja: '交渉における理解', ko: '협상에서의 이해', ms: 'Pemahaman Rundingan', hi: 'बातचीत में समझ', ar: 'فهم التفاوض', es: 'Comprensión en Negociación', de: 'Verhandlungsverständnis', fr: 'Compréhension en Négociation', it: 'Comprensione nella Negoziazione',
    },
    persuade: {
      en: 'Persuasion Through Empathy', zh: '通过共情进行说服', ja: '共感を通じた説得', ko: '공감을 통한 설득', ms: 'Pujukan Melalui Empati', hi: 'सहानुभूति के माध्यम से समझाना', ar: 'الإقناع من خلال التعاطف', es: 'Persuasión con Empatía', de: 'Überzeugung durch Empathie', fr: 'Persuasion par Empathie', it: 'Persuasione attraverso l\'Empatia',
    },
    readroom: {
      en: 'Reading the Room', zh: '洞察现场氛围', ja: '場の空気を読む', ko: '분위기 파악', ms: 'Membaca Suasana', hi: 'कमरे को पढ़ना', ar: 'قراءة الأجواء', es: 'Leer la Sala', de: 'Die Stimmung erahnen', fr: 'Lire la Pièce', it: 'Leggere la Stanza',
    },
  },

  // ═══════════════════════════════════════════════
  // Sun Tzu Scenarios
  // ═══════════════════════════════════════════════
  sunzuScenarios: {
    landscape: {
      en: 'Competitive Landscape', zh: '竞争格局分析', ja: '競争環境の分析', ko: '경쟁 환경 분석', ms: 'Landskap Persaingan', hi: 'प्रतिस्पर्धा परिदृश्य', ar: 'المشهد التنافسي', es: 'Paisaje Competitivo', de: 'Wettbewerbslandschaft', fr: 'Paysage Compétitif', it: 'Panorama Competitivo',
    },
    positioning: {
      en: 'Strategic Positioning', zh: '战略性定位', ja: '戦略的ポジショニング', ko: '전략적 포지셔닝', ms: 'Posisi Strategik', hi: 'रणनीतिक स्थिति', ar: 'الموضع الاستراتيجي', es: 'Posicionamiento Estratégico', de: 'Strategische Positionierung', fr: 'Positionnement Stratégique', it: 'Posizionamento Strategico',
    },
    dynamics: {
      en: 'Reading Competitive Dynamics', zh: '洞察竞争动态', ja: '競争動向の理解', ko: '경쟁 역학 파악', ms: 'Membaca Dinamik Persaingan', hi: 'प्रतिस्पर्धा गतिशीलता को पढ़ना', ar: 'قراءة الديناميكيات التنافسية', es: 'Leyendo la Dinámica Competitiva', de: 'Wettbewerbsdynamiken verstehen', fr: 'Comprendre la Dynamique Concurrentielle', it: 'Comprendere la Dinamica Competitiva',
    },
  },

  // ═══════════════════════════════════════════════
  // Cialdini Scenarios
  // ═══════════════════════════════════════════════
  cialdiniScenarios: {
    ethical: {
      en: 'Ethical Influence in Practice', zh: '伦理影响力的实践', ja: '倫理的影響力の実践', ko: '윤리적 영향력 실천', ms: 'Pengaruh Etika dalam Amalan', hi: 'नैतिक प्रभाव का अभ्यास', ar: 'التأثير الأخلاقي في الممارسة', es: 'Influencia Ética en la Práctica', de: 'Ethischer Einfluss in der Praxis', fr: 'Influence Éthique en Pratique', it: 'Influenza Etica nella Pratica',
    },
    trust: {
      en: 'Building Genuine Trust', zh: '建立真诚的信任', ja: '真の信頼を築く', ko: '진정한 신뢰 구축', ms: 'Membina Kepercayaan Sebenar', hi: 'ईमानदार विश्वास बनाना', ar: 'بناء الثقة الحقيقية', es: 'Construyendo Confianza Genuina', de: 'Vertrauen aufbauen', fr: 'Bâtir une Confiance Authentique', it: 'Costruire Fiducia Genuina',
    },
    objections: {
      en: 'Overcoming Objections with Respect', zh: '尊重地回应异议', ja: '敬意を持って異議に対応する', ko: '존중으로 이의 극복', ms: 'Mengatasi Bantahan dengan Hormat', hi: 'सम्मान के साथ आपत्तियों को दूर करना', ar: 'التغلب على الاعتراضات باحترام', es: 'Superando Objeciones con Respeto', de: 'Einwände respektvoll überwinden', fr: 'Surmonter les Objections avec Respect', it: 'Superare le Obiezioni con Rispetto',
    },
  },

  // ═══════════════════════════════════════════════
  // Biases Scenarios
  // ═══════════════════════════════════════════════
  biasesScenarios: {
    recognize: {
      en: 'Recognizing Manipulation', zh: '识别操纵行为', ja: '操作の識別', ko: '조작 인식', ms: 'Mengenali Manipulasi', hi: 'हेरफेर की पहचान', ar: 'التعرف على التلاعب', es: 'Reconociendo la Manipulación', de: 'Manipulation erkennen', fr: 'Reconnaître la Manipulation', it: 'Riconoscere la Manipolazione',
    },
    informed: {
      en: 'Informed Decision-Making', zh: '知情决策', ja: '情報に基づいた意思決定', ko: '정보에 기반한 의사결정', ms: 'Pembuatan Keputusan Berinformasi', hi: 'सूचित निर्णय लेना', ar: 'اتخاذ قرارات مستنيرة', es: 'Toma de Decisiones Informada', de: 'Informierte Entscheidungsfindung', fr: 'Prise de Décision Éclairée', it: 'Presa di Decisioni Informatà',
    },
    selfcheck: {
      en: 'Self-Awareness Check', zh: '自我觉察检查', ja: '自己認識チェック', ko: '자기인식 점검', ms: 'Semakan Kesedaran Diri', hi: 'आत्म-जागरूकता जांच', ar: 'فحص الوعي الذاتي', es: 'Verificación de Autoconciencia', de: 'Selbstreflexion', fr: 'Vérification de Conscience de Soi', it: 'Verifica di Consapevolezza',
    },
  },

  // ═══════════════════════════════════════════════
  // Available Languages
  // ═══════════════════════════════════════════════
  languages: {
    en:'English', zh:'中文', ja:'日本語', ko:'한국어', ms:'Bahasa Melayu',
    hi:'हिन्दी', ar:'العربية', es:'Español', de:'Deutsch', fr:'Français', it:'Italiano',
  },
};

module.exports = i18n;
