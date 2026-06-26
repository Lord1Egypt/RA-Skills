#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 乱码修复模块
使用 LLM 根据上下文推断和修复乱码字符
"""

import json
import re
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# 导入 LLM 客户端
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import LLMClient, get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MojibakeFixResult:
    """乱码修复结果"""
    original: str
    fixed: str
    changes: List[Dict]
    confidence: float
    success: bool


# 乱码修复 Prompt 模板
MOJIBAKE_FIX_PROMPT = """# 角色
你是一个专业的文本修复专家，擅长根据上下文推断和修复乱码字符。

# 任务
修复以下文本中的乱码字符。

# 修复原则
1. 根据上下文语义推断正确字符
2. 保持句子通顺和语义完整
3. 无法确定的内容标记为 [无法识别]
4. 不要修改非乱码的正常字符

# 常见乱码特征
- 鏈、銆、鈥、锛、熲 等生僻字通常是编码错误
- å、æ、ç 开头的字符通常是 UTF-8 编码错误
- 连续的"拷"字通常是"锟斤拷"问题
- 乱码通常出现在引号、标点、特殊字符位置

# 输出格式（仅输出 JSON，不要其他内容）
{{"original": "原文", "fixed": "修复后的文本", "changes": [{{"position": "位置索引", "before": "乱码", "after": "修复后", "reason": "推断理由"}}], "confidence": 0.9}}

# 待修复文本
{text}"""

# 批量乱码修复 Prompt 模板
BATCH_MOJIBAKE_FIX_PROMPT = """# 角色
你是一个专业的文本修复专家，擅长根据上下文推断和修复乱码字符。

# 任务
修复以下多个文本片段中的乱码字符。

# 修复原则
1. 根据上下文语义推断正确字符
2. 保持句子通顺和语义完整
3. 无法确定的内容标记为 [无法识别]
4. 不要修改非乱码的正常字符

# 常见乱码特征
- 鏈、銆、鈥、锛、熲 等生僻字通常是编码错误
- å、æ、ç 开头的字符通常是 UTF-8 编码错误
- 连续的"拷"字通常是"锟斤拷"问题

# 输出格式（仅输出 JSON 数组，不要其他内容）
[
  {{"index": 0, "original": "原文", "fixed": "修复后", "changes": [...], "confidence": 0.0-1.0}},
  {{"index": 1, "original": "原文", "fixed": "修复后", "changes": [...], "confidence": 0.0-1.0}},
  ...
]

# 待修复文本列表
{texts}"""


class AIMojibakeFixer:
    """AI 乱码修复器"""
    
    def __init__(self, config: Dict, llm_client: Optional[LLMClient] = None):
        self.config = config.get('ai_enhancement', {}).get('mojibake_fix', {})
        self.enabled = self.config.get('enabled', True)
        self.batch_size = self.config.get('batch_size', 5)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.7)
        self.auto_learn = self.config.get('auto_learn', True)
        self.max_fixes = self.config.get('max_fixes', 50)
        
        # LLM 客户端
        self.llm = llm_client or get_client(config)
        
        # 学习到的规则
        self.learned_rules: Dict[str, str] = {}
        self._load_learned_rules()
        
        # 统计信息
        self.fixed_count = 0
        self.total_processed = 0
    
    def fix(self, text: str) -> MojibakeFixResult:
        """修复文本中的乱码"""
        if not self.enabled:
            logger.info("AI 乱码修复已禁用")
            return MojibakeFixResult(
                original=text,
                fixed=text,
                changes=[],
                confidence=0.0,
                success=False
            )
        
        # 先用规则引擎修复
        rule_fixed, rule_changes = self._rule_fix(text)
        
        # 检查是否还有乱码
        remaining_mojibake = self._detect_mojibake(rule_fixed)
        
        if not remaining_mojibake:
            # 规则引擎已全部修复，无需调用 LLM
            logger.info("规则引擎已修复所有乱码，无需 AI 介入")
            return MojibakeFixResult(
                original=text,
                fixed=rule_fixed,
                changes=rule_changes,
                confidence=1.0,
                success=True
            )
        
        # 只有当规则引擎无法修复时才调用 LLM
        logger.info(f"发现 {len(remaining_mojibake)} 处未知乱码，调用 AI 修复")
        
        # AI 修复剩余乱码
        ai_result = self._ai_fix(rule_fixed)
        
        # 合并结果
        all_changes = rule_changes + ai_result.changes
        
        # 学习新规则
        if self.auto_learn and ai_result.confidence > 0.9:
            self._learn_from_fix(ai_result)
        
        self.fixed_count += len(all_changes)
        self.total_processed += 1
        
        return MojibakeFixResult(
            original=text,
            fixed=ai_result.fixed,
            changes=all_changes,
            confidence=ai_result.confidence,
            success=True
        )
    
    def fix_batch(self, texts: List[str]) -> List[MojibakeFixResult]:
        """批量修复"""
        results = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_results = self._ai_fix_batch(batch)
            results.extend(batch_results)
        return results
    
    def _rule_fix(self, text: str) -> Tuple[str, List[Dict]]:
        """规则引擎快速修复"""
        changes = []
        fixed_text = text
        
        # 已知乱码映射
        mojibake_map = {
            # GBK → UTF-8 编码错误
            '鏈枃': '本文',
            '銆€銆€': '',
            '銆€': '',
            '鈥斅': '——',
            # 引号乱码
            '鈥溄': '"',
            '鈥澨': '"',
            '鈥橈拷': "'",
            '锛堬拷': '（',
            '锛堬拷': '）',
            '銆愩': '【',
            '銆愩': '】',
            # 标点乱码
            '锛€': '，',
            '锛': '，',
            '锛': '。',
            '锛': '？',
            '锛': '！',
            '锛': '：',
            '锛': '；',
            '锛': '、',
            '熲': '？',
            # 单字符乱码
            '鈥': '"',
            '鈥': '"',
            '銆': '',
            '溄': '"',
            '澨': '"',
            '堬拷': '',
            '拷': '',
            # UTF-8 编码错误（精确映射）
            'å…³': '关',
            'åœ¨': '在',
            'æœ‰': '有',
            'å•Š': '啊',
            'çŽ°': '现',
            '锟斤拷': '',
            '锟斤': '',
        }
        
        # 合并学习到的规则
        all_rules = {**mojibake_map, **self.learned_rules}
        
        for mojibake, correct in all_rules.items():
            if mojibake in fixed_text:
                count = fixed_text.count(mojibake)
                fixed_text = fixed_text.replace(mojibake, correct)
                changes.append({
                    'before': mojibake,
                    'after': correct,
                    'count': count,
                    'method': 'rule'
                })
        
        # 特殊字符处理
        # BOM 标记
        if '\ufeff' in fixed_text:
            fixed_text = fixed_text.replace('\ufeff', '')
            changes.append({'before': '\\ufeff', 'after': '', 'count': 1, 'method': 'rule'})
        
        # 替换字符
        if '�' in fixed_text:
            fixed_text = fixed_text.replace('�', '')
            changes.append({'before': '�', 'after': '', 'count': 1, 'method': 'rule'})
        
        # 连续屯字
        tun_pattern = r'屯{2,}'
        if re.search(tun_pattern, fixed_text):
            fixed_text = re.sub(tun_pattern, '', fixed_text)
            changes.append({'before': '屯+', 'after': '', 'count': 1, 'method': 'rule'})
        
        # 生僻字填充乱码 - 直接删除
        rare_char_sequences = self._detect_rare_char_filler(fixed_text)
        for seq in rare_char_sequences:
            if seq in fixed_text:
                count = fixed_text.count(seq)
                fixed_text = fixed_text.replace(seq, '')
                changes.append({
                    'before': seq[:20] + '...' if len(seq) > 20 else seq,
                    'after': '',
                    'count': count,
                    'method': 'rare_char_rule',
                    'length': len(seq)
                })
                logger.info(f"删除生僻字填充乱码: {len(seq)} 字符")
        
        return fixed_text, changes
    
    def _detect_mojibake(self, text: str) -> List[str]:
        """检测文本中的乱码"""
        mojibake_patterns = [
            r'[鏈銆鈥锛熲溄澨堬拷]+',  # GBK 编码错误
            r'[åæç][^a-zA-Z\s]{2,}',  # UTF-8 编码错误
            r'锟斤拷',  # 经典乱码
            r'�+',  # 替换字符
            r'屯{2,}',  # 连续屯字
        ]
        
        found = []
        for pattern in mojibake_patterns:
            matches = re.findall(pattern, text)
            found.extend(matches)
        
        # 检测生僻字填充乱码
        rare_char_patterns = self._detect_rare_char_filler(text)
        found.extend(rare_char_patterns)
        
        return list(set(found))
    
    def _detect_rare_char_filler(self, text: str) -> List[str]:
        """检测生僻字填充乱码"""
        # 定义罕见字/生僻字范围（CJK 扩展区）
        # 这些字符在正常中文文本中极少出现
        rare_char_ranges = [
            (0x3400, 0x4DBF),   # CJK 扩展A
            (0x20000, 0x2A6DF), # CJK 扩展B（需要特殊处理）
            (0x2A700, 0x2B73F), # CJK 扩展C
            (0x2B740, 0x2B81F), # CJK 扩展D
            (0x2B820, 0x2CEAF), # CJK 扩展E
            (0x2CEB0, 0x2EBEF), # CJK 扩展F
        ]
        
        # 常见的生僻字填充字符（从实际乱码文件中提取）
        known_filler_chars = set('牙笫歁睅紒煸睈粑猷欃笌紾簠灰狣歱爲毌澺硃猀猻猼猽獀獁獂獃獄獆獇獈獉獊獋獌獍獎獏獐獑獒獓獔獕獖獗獘獙獚獛獜獝獞獟獠獡獢獣獤獥獦獧獨獩獪獫獬獭獮獯獱獲獳獴獵獶獷獸獹獺獻獼獽獾獿玀玁玂玃玅玆玈玊玌玍玏玐玑玒玓玔玕玖玗玘玙玚玛玜玝玞玟玠玡玢玣玤玥玧玨玪玬玭玱玲玳玴玵玶玷玸玹玺玻玼玽玾玿珀珁珂珃珄珅珆珇珈珉珊珋珌珍珎珏珐珑珒珓珔珕珖珗珘珙珚珛珜珝珞珟珠珡珢珣珤珥珦珧珨珩珪珫珬班珮珯珰珱珲珳珴珵珶珷珸珹珺珻珼珽現珿琀琁琂球琄琅理琇琈琉琊琋琌琍琎琏琐琑琒琓琔琕琖琗琘琙琚琛琜琝琞琟琠琡琤琥琧琨琩琫琬琭琮琯琱琲琷琸琹琺琻琼琽琾琿瑀瑁瑂瑃瑄瑅瑆瑇瑈瑉瑊瑋瑌瑍瑎瑏瑐瑑瑒瑓瑔瑕瑖瑘瑝瑠瑡瑢瑣瑤瑥瑦瑧瑨瑩瑪瑫瑬瑭瑮瑱瑲瑳瑴瑵瑸瑹瑺瑻瑼瑽瑾瑻璂璄璅璆璈璉璊璌璍璏璑璒璓璔璕璖璗璘璙璚璛璝璟璠璡璢璣璤璥璦璪璫璬璭璮璯环璱璲璳璴璵璶璷璸璹璻璼璽璾璿瓀瓁瓂瓃瓄瓅瓆瓇瓈瓉瓊瓋瓌瓍瓎瓏瓐瓑瓓瓔瓕瓖瓗瓘瓙瓚瓛瓝瓟瓡瓥瓧瓨瓩瓪瓫瓬瓭瓳瓵瓸瓹瓺瓻瓼瓽瓾甀甁甂甃甅甆甇甈甉甊甋甌甍甎甏甐甑甒甓甔甕甖甗甘甙甝甞甠甡產甤甦甧甪甮甴甶甹甼甽甾甿畁畂畃畄畆畇畉畊畋界畍畎畐畑畒畓畕畖畗畘畝畞畟畠畡畢畣畤畧畨畩畫畬畭畮畯畱畳畵當畷畸畹畺畻畼畽畾疀疁疂疄疅疇疈疉疊疋疌疍疎疐疓疕疘疛疜疞疢疦疧疨疩疪疭疳疴疶疷疺疻疿痀痁痂痃痄痆症痈痉痐痑痓痗痙痚痜痝痟痠痡痥痩痬痭痮痯痯痰痱痲痳痵痸痻痽痾瘂瘄瘅瘇瘈瘉瘊瘋瘌瘍瘎瘏瘑瘒瘓瘔瘕瘖瘗瘘瘙瘚瘜瘝瘞瘡瘣瘤瘥瘨瘬瘭瘮瘯瘱瘲瘳瘴瘵瘶瘷瘸瘹瘺瘻瘼瘽瘿癀癁療癃癄癅癆癇癈癉癊癋癎癏癐癑癒癓癕癗癘癙癚癛癝癠癡癢癤癥癦癧癨癩癪癬癭癮癯癰癱癲癳癴癵癶癷癸癹発登癿皀皁皃皅皉皊皌皍皏皐皒皔皕皗皘皚皛皜皝皞皟皠皡皢皣皥皦皧皨皩皪皫皬皭皯皰皳皵皶皷皸皹皺皻皼皽皾盀盁盂盃盄盅盇盉盋盌盓盕盙盚盜盝盞盠盡盢監盤盥盦盧盨盩盪盫盬盭盰盱盳盵盶盷盺盻盽盿眀眂眃眄眅眆眇眈眉眊眎眏眐眑眒眓眔眕眖眗眘眛眜眝眞眡眣眤眥眦眧眪眫眬眮眰眱眲眳眴眹眻眽眾着睂睃睅睆睈睉睊睋睌睍睎睏睒睓睔睕睖睗睘睙睜睝睞睠睡睢睤睥睧睨睩睪睭睮睯睰睱睲睳睴睵睶睸睺睼睽睾瞀瞁瞂瞃瞆瞇瞈瞉瞊瞋瞌瞍瞏瞐瞓瞔瞕瞖瞗瞘瞙瞚瞛瞜瞝瞞瞡瞣瞤瞦瞨瞫瞭瞮瞯瞱瞲瞴瞶瞷瞸瞹瞺瞻瞼瞽瞾矀矁矂矃矄矅矆矇矈矉矊矋矌矍矎矏矐矑矒矓矔矕矖矘矙矚矝矞矟矠矡矤矦矨矪矬矰矱矲石矴矵矷矹矺矻矼矽矾矿砀砈砉砊砋砎砏砐砑砒砓砕砗砘砙砚砛砜砞砠砡砢砣砤砦砧砨砩砪砫砮砯砰砱砲砳砵砶砷砀砹砺砼砽砾砿础硁硂硃硄硅硆硇硈硉硊硋硌硍硎硏硐硑硒硓硔硕硖硗硘硙硚硛硜硝硞硟硡硢硣硤硥硦硧硨硩硪硫硬硭确硯硰硱硲硳硴硵硶硷硸硹硺硻硼硽硾硿碀碁碂碃碄碅碆碇碈碉碊碋碌碍碏碐碒碔碕碖碗碘碙碚碛碜碝碞碠碢碣碤碥碦碧碨碩碪碫碬碭碮碯碵碶磅碸碹確碻碼碽碾碿磀磂磃磄磆磇磈磉磌磍磎磏磑磒磓磖磗磘磚磛磜磝磞磟磠磡磢磣磤磥磦磧磩磪磫磬磭磮磯磰磱磳磶磸磹磻磼磽磾磿礀礂礃礄礆礇礈礉礊礋礌礍礎礏礐礑礒礔礕礖礗礘礙礚礛礜礝礞礟礠礡礢礣礥礦礧礨礩礪礫礬礭礮礯礰礱礲礳礴礵礶礷礸礹礽礿祂祃祄祅祆祇祈祉祊祋祌祍祎祏祐祑祒祔祕祘祙祚祛祜祝神祟祡祣祤祦祧祩祪祫祬祮祰祱祲祳祴祵祶祹祻祼祽祾祿禂禃禇禈禉禋禌禍禎禐禑禒禓禔禕禖禗禘禙禛禜禝禞禟禠禡禢禣禤禥禦禨禩禪禫禬禭禮禯禰禱禲禴禵禶禷禸禼禿秂秄秅秇秈秊秌种秎秏秐秓秔秖秗秙秚秛秜秝秞秠秡秢秥秨秪秬秮秱秲秳秴秵秶秷秹秺秼秾秿稁稄稅稆稇稈稉稊稌稏稐稑稒稓稕稖稘稙稛稜稝稞稡稢稤稥稦稧稨稩稪稫稬稭種稯稰稱稲稴稵稶稸稺稾穁穂穃穄穅穆穇穈穉穊穋穌穕穖穘穙穚穛穜穝穞穟穠穡穢穣穤穥穦穧穨穩穪穫穬穭穮穯穰穱穲穳穵穸穻穼穽穾窂窅窆窇窈窉窊窋窌窎窏窐窓窔窚窛窞窡窢窤窧窨窩窪窫窬窮窯窰窱窲窴窵窶窷窸窹窺窻窼窽窾竀竁竂竃竄竅竆竇竈竉竊竌竍竎竏竐竑竒竓竕竗竘竚竛竜竝竡竢竤竧竨竩竪竫竬竮竰竱竲竳竴竵競竷竸竻竼竾笀笁笂笄笅笆笇笉笌笍笎笐笒笓笕笖笗笘笚笜笝笟笡笢笣笧笩笭笮笯笰笲笴笵笶笷笹笺笻笽笾笿筀筁筂筃筄筆筈筊筍筎筓筕筗筙筚筞筟筡筣筤筥筦筧筨筩筪筫筬筭筯筰筳筴筶筸筺筻筼筽筿箁箂箃箄箆箇箈箉箊箎箏箐箑箒箓箖箘箙箚箛箞箟箠箣箤箥箮箯箰箲箳箵箶箷箹箺箻箼箽箾箿節篂篃範篅篆篈篊篋篍篎篏篐篑篒篔篕篖篗篘篛篜篞篟篠篢篣篤篥篦篧篨篩篪篫篬篭篯篰篲篳篴篵篶篸篹篺篻篽篿簀簁簂簃簄簅簆簈簉簊簋簌簍簎簏簐簑簒簓簔簕簗簘簙簚簛簜簝簞簠簡簢簣簤簥簦簧簨簩簪簫簬簭簮簯簰簱簲簳簴簵簶簷簸簹簺簻簼簽簾籀籁籂籃籄籅籆籇籈籉籊籋籌籍籎籏籐籑籒籓籔籕籖籗籘籙籚籛籜籝籞籟籠籡籢籣籤籥籦籧籨籩籪籫籬籭籮籯籰籱籲米籴籵籶籷籸籹籺籾籿粀粁粂粃粄粅粆粇粈粊粌粍粎粏粐粓粔粖粙粚粛粠粡粣粦粧粨粩粫粬粭粯粰粴粵粶粷粸粺粻粼粿糀糁糂糃糄糅糆糇糈糉糎糏糐糑糒糓糔糘糚糛糝糞糡糢糣糤糥糦糧糩糪糫糬糭糮糰糱糲糳糴糵糶糷糹糺糼糽糾糿紀紁紂紃約紅紆紇紈紉紊紋紌納紎紏紐紑紒紓純紕紖紗紘紙級紛紜紝紞紟素紡紣紤紥紦紨紩紪紬紭紮累細紱紲紳紴紵紶紷紸紹紺紻紼紽紾紿絀絁終絃組絅絆絇絈絉絊絋経絍絎絏絑絒絓絔絕絖絗絘絙絚絛絜絝絞絟絠絡絢絣絤絥給絧絨絩絪絫絬絭絮絯絰統絲絳絴絵絶絷絸絹絺絻絼絽絾絿綀綁綂綃綄綅綆綇綈綉綊綋綌綍綎綏綐綑綒經綔綕綖綗綘継続綛綜綝綞綟綠綡綢綣綤綥綦綧綨綩綪綫綬維綮綯綰綱網綳綴綵綶綷綸綹綺綻綼綽綾綿緀緁緂緃緄緅緆緇緈緉緊緋緌緍緎総緐緑緔緕緖緗緘緙線緛緜緝緞緟締緡緢緣緤緥緦緧編緩緪緫緬緭緮緯緰緱緲緳練緵緶緷緸緹緺緻緼緽緾緿縀縁縂縃縄縅縆縇縈縉縊縋縌縍縎縏縐縑縒縓縔縕縖縗縘縙縚縛縜縝縞縟縠縡縢縣縤縥縦縧縨縩縪縫縬縭縮縯縰縱縲縳縴縵縶縷縸縹縺縻縼總績縿繀繁繂繃繄繅繆繇繈繉繊繋繌繍繎繏繐繑繒繓織繕繖繗繘繙繚繛繜繝繞繟繠繡繢繣繤繥繦繧繨繩繪繫繬繭繮繯繰繱繲繳繴繵繶繷繸繹繺繻繼繽繾繿纀纁纂纃纄纅纆纇纈纉纊纋續纍纎纏纐纑纒纓纔纕纖纗纘纙纚纜纝纞纟纠纡红纣纤纥约级纨纩纪纫纬纭纮纯纰纱纲纳纴纵纶纷纸纹纺纻纼纽纾线缁缂缃缄缅缆缇缈缉缊缋缌缍缎缏缐缑缒缓缔缗缙缛缜缝缞缟缡缢缣缤缥缦缧缨缩缪缫缬缭缯缰缱缲缳缴缵缶缷缸缹缻缼缽缾缿罀罁罂罃罄罅罆罇罈罉罊罋罌罍罎罏罒罓罔罖罘罙罚罛罜罝罞罟罠罡罢罣罤罥罦罧罨罩罪罫罬罭置罯罰罱罳罴罵罶罸罹罺罻罼罽罾罿羀羂羃羄羅羆羇羈羉羊羋羍羏羐羑羒羓羕羖羗羘羙羛羜羝羞羠羡羢羣羥羦羨羪羫羬羭羮羱羳羴羵羷羸羺羻羾羿翀翂翃翄翆翇翈翉翋翍翏翐翑翓翖翗翙翚翛翜翝翞翠翢翣翤翥翦翧翨翪翫翬翭翯翲翴翵翶翷翸翹翺翻翼翽翾翿耂耇耈耉耓耚耛耝耞耟耡耣耤耥耫耬耭耮耯耰耱耲耴耹耺耼耾聀聁聂聃聄聅聇聈聉聎聏聐聑聓聕聖聗聙聛聜聝聟聠聡聢聣聤聥聦聧聨聫聬聭聮聯聰聱聲聳聴聵聶職聸聹聺聻聼聽聾聿肁肂肄肅肈肊肍肎肏肐肑肒肓肔肕肗肞肣肦肧肨肬肰肳肵肶肸肹肻肼肾肿肤肻肼肾肿脀脁脂脃脄脅脆脇脈脋脌脎脏脗脙脜脝脟脠脡脢脣脤脥脦脧脨脩脪脫脭脮脰脳脴脵脷脹脺脻脼脽脿腀腁腂腃腄腅腆腇腉腊腖腗腘腛腜腝腞腟腡腢腣腤腦腨腪腬腲腳腴腵腶腷腸膁膂膃膄膅膆膇膉膋膌膍膎膒膓膔膕膖膗膙膚膞膟膡膢膤膥膧膩膪膬膭膮膰膱膲膴膶膷膸膹膼膽膾膿臄臅臇臈臉臋臍臎臏臐臑臒臓臔臕臖臗臘臙臚臛臜臝臞臟臠臡臢臤臥臦臨臩臫臬臮臯臰臱臲臵臶臷臸臹臺臼臽臾臿舀舁舂舃舄舎舏舐舑舓舕舖舙舚舝舠舡舢舣舤舥舦舧舩舮舺舼舽舿艀艁艂艃艅艆艈艊艌艍艎艐艑艒艓艔艕艖艗艛艜艝艞艠艡艢艣艤艥艦艧艩艪艫艬艭艱艵艶艷艸艻艼艽艾艿芀芁芃芅芆芇芉芌芐芑芔芕芖芚芛芞芠芢芣芧芨芩芪芫芬芴芵芶芺芻芼芿苀苂苃苅苆苉苐苖苙苚苝苢苤苨苪苬苭苮苰苲苳苵苸苺苼苽苾苿茀茊茋茍茐茒茓茖茘茙茝茞茟茠茡茢茣茤茥茦茩茪茮茰茲茷茻茽茾茿荀荁荂荄荅荈荊荋荌荍荎荓荕荖荗荘荙荝荢荣荥荦荩荪荬荭荮荱荲荳荴荵荶荹荺荾荿莀莁莂莃莄莇莈莊莋莌莍莏莐莑莔莕莖莗莙莝莡莢莣莤莥莦莧莬莭莮莯莰莱乐莻莼莾莿菂菃菄菆菈菉菋菍菎菐菑菒菓菕菗菙菚菛菞菢菣菤菦菧菨菫菬菭恰菮菳菴菵菶菷菸菹菺菻菼菾菿萀萂萅萇萈萉萊萐萒萓萔萕萖萗萘萙萚萛萞萠萡萢萣萪萫萩萲萳萴萵萶萷萹萺萻萾萿葀葁葂葃葄葅葇葈葊葋葌葍葎葏葑葒葓葔葕葖葘葝葞葟葠葢葤葥葦葧葨葪葮葯葰葲葳葴葶葸葺葻葼葽葾葿蒀蒁蒃蒄蒅蒆蒊蒋蒌蒍蒎蒏蒐蒑蒒蒓蒔蒕蒖蒘蒚蒛蒝蒞蒟蒠蒢蒣蒤蒥蒦蒧蒨蒩蒪蒫蒬蒭蒮蒰蒱蒳蒴蒵蒶蒷蒻蒼蒾蓀蓁蓂蓃蓅蓆蓇蓈蓊蓋蓌蓎蓏蓒蓔蓕蓗蓚蓛蓜蓞蓡蓢蓤蓥蓦蓧蓨蓩蓪蓫蓭蓮蓯蓱蓲蓳蓴蓵蓶蓷蓸蓹蓺蓻蓼蓾蓿蔀蔁蔂蔃蔅蔆蔇蔈蔉蔊蔋蔌蔍蔎蔏蔐蔒蔔蔕蔖蔘蔙蔛蔜蔝蔞蔠蔢蔣蔤蔥蔦蔧蔨蔩蔪蔭蔮蔯蔰蔱蔲蔳蔴蔵蔶蔸蔹蔺蔻蔼蔽蔾蔿蕀蕁蕂蕃蕄蕅蕆蕇蕈蕉蕋蕌蕍蕎蕏蕐蕑蕒蕓蕔蕕蕗蕘蕚蕛蕜蕝蕞蕟蕠蕡蕢蕣蕥蕦蕧蕩蕪蕫蕬蕭蕮蕯蕰蕱蕳蕵蕶蕷蕸蕼蕽蕿薀薁薂薃薆薈薉薋薌薍薎薐薑薒薓薔薕薖薗薘薙薚薝薞薟薠薡薢薣薥薦薧薩薫薭薮薱薲薳薴薵薶薸薺薻薼薽薾薿藀藂藃藄藅藆藇藈藊藋藌藍藎藑藒藔藖藗藘藙藚藛藝藞藟藠藡藢藣藦藧藨藪藫藬藭藮藯藰藱藲藳藴藵藶藷藸藹藺藼藽藾藿蘀蘁蘂蘃蘄蘆蘇蘈蘉蘊蘋蘌蘍蘎蘏蘐蘒蘓蘔蘕蘗蘙蘚蘛蘜蘝蘞蘟蘠蘡蘢蘣蘤蘥蘦蘨蘪蘫蘬蘭蘮蘯蘰蘱蘲蘳蘴蘵蘶蘷蘸蘹蘺蘻蘽蘾蘿虀虁虂虃虄虅虆虇虈虉虊虋虌虒虓虖虗虘虙虛虜虝虞虡虣虤虥虦虧虨虩虪虭虯虰虲虳虴虵虶虷虸虹虺虻虼虽虿蚇蚈蚉蚎蚏蚐蚑蚒蚔蚖蚗蚘蚙蚚蚛蚞蚟蚠蚡蚢蚥蚦蚫蚭蚮蚲蚳蚴蚵蚶蚸蚹蚺蚻蚼蚽蚾蚿蛁蛂蛃蛅蛆蛈蛉蛌蛍蛒蛓蛕蛖蛗蛚蛜蛝蛠蛡蛢蛣蛥蛦蛨蛪蛫蛬蛯蛵蛶蛷蛸蛺蛼蛽蛿蜁蜄蜅蜆蜋蜌蜎蜏蜐蜑蜔蜖蜙蜛蜝蜟蜠蜤蜦蜧蜨蜪蜫蜬蜭蜯蜰蜲蜳蜄蜅蜆蜇蜈蜉蜊蜋蜌蜍蜎蜏蜐蜑蜒蜓蜔蜕蜖蜗蜘蜙蜛蜝蜞蜟蜠蜡蜢蜣蜤蜥蜦蜧蜨蜪蜫蜬蜭蜯蜰蜲蜳蜴蜵蜶蜷蜸蜹蜺蜼蜽蜾蜿蝀蝁蝂蝃蝄蝅蝆蝊蝋蝍蝏蝐蝑蝒蝔蝕蝖蝘蝚蝛蝜蝝蝞蝟蝡蝢蝦蝧蝨蝩蝪蝫蝬蝭蝯蝰蝲蝳蝵蝷蝸蝹蝺蝻蝿螀螁螄螆螇螉螊螌螎螏螐螑螒螔螕螖螘螙螚螛螜螝螞螠螡螢螣螤螥螦螧螩螪螫螬螭螮螱螲螴螶螷螸螹螻螼螾螿蟁蟂蟃蟄蟅蟆蟇蟈蟉蟌蟍蟎蟏蟐蟔蟕蟖蟗蟘蟙蟚蟜蟝蟞蟡蟢蟣蟤蟦蟧蟨蟩蟫蟪蟫蟬蟭蟯蟰蟱蟲蟴蟶蟷蟸蟳蟻蟽蟿蠀蠁蠂蠄蠅蠆蠇蠈蠉蠋蠌蠍蠎蠏蠐蠑蠒蠓蠔蠖蠗蠘蠙蠚蠜蠝蠞蠟蠠蠡蠢蠣蠥蠦蠧蠨蠩蠪蠫蠬蠭蠮蠯蠰蠱蠳蠴蠵蠶蠸蠺蠻蠽蠾蠿衁衂衃衆衇衈衉衎衐衑衒衕衖衘衚衜衞衟衠衦衧衪衭衯衱衲衴衵衶衸衹衺衻衼衽衾衿袀袁袂袃袄袆袇袈袉袊袋袌袎袏袐袑袒袓袔袕袗袘袙袚袛袝袞袟袠袡袣袥袦袧袨袩袪小袬袮袯袰袲袳袴袵袶袸袹袺袻袼袽袾袿裀裃裄裇裈裊裋裌裍裏裐裑裓裖裗裚裛補裞裠裡裦裧裩裪裫裬裭裮裯裲裵裶裷裺裻製裿褀褁褃褄褅褆複褉褋褌褍褎褏褑褔褕褖褗褘褜褝褞褟褠褢褣褤褦褧褨褩褬褭褮褯褱褲褳褵褷褸褹褺褻褼褽褾褿襀襁襂襃襅襆襇襈襉襊襋襌襍襎襏襐襑襒襓襔襕襗襘襙襚襛襜襝襠襡襢襣襤襥襧襨襩襪襫襬襭襮襯襰襱襲襳襴襵襶襷襸襹襺襼襽襾西覀要覂覃覄覅覆覇覈覉覊見覌覍覎規覐覑覒覓覔覕覗覘覙覚覛覜覝覞覟覠覡覢覣覤覥覦覧覨覩親覫覬覭覮覯覰覱覲観覴覵覶覷覸覹覺覻覼覽覾覿觀觃规觅视觇觊觋觌觍觎觏觐觑角觓觔觕觗觘觙觚觛觜觝觞觟觠觡觢觤觧觨觩觪觬觭觮觰觱觲觳觴觵觶觷觸觹觺觻觼觽觾觿訁訂訃訄訅訆計訉訊訋訌訍討訏訐訑訒訓訔訕訖託記訙訚訛訜訝訞訟訠訡訢訣訤訥訦訧訨訩訪訫訬設訮訯訰許訲訳訴訵訶訷訸訹詂詃詄詅詆詇詈詉詊詋詌詍詎詏詐詑詒詓詔評詖詗詘詙詚詛詜詝詞詟詠詡詢詣詤詥試詧詩詪詫詬詭詮詯詰話該詳詴詵詶詷詸詺詻詼詽詾詿誀誁誂誃誄誅誆誇誈誋誌認誎誏誐誑誒誔誕誖誗誘誙誚誛誜誝語誟誠誡誢誣誤誥誦誧誨誩說誫説読誮誯誰誱誳誴誶誷誸誹誺誻誼誽誾調諀諁諂諃諄諅諆談諈諉諊請諌諍諎諏諐諑諒諓諔諕諗諘諙諚諛諜諝諞諟諠諡諢諣諤諥諦諧諨諩諪諫諬諭諮諯諰諱諲諳諴諵諶諷諸諹諺諻諼諽諾諿謀謁謂謃謄謅謆謇謈謉謊謋謌謍謎謏謐謑謒謓謔謕謖謗謘謙謚講謜謝謞謟謠謡謢謣謤謥謧謨謩謪謫謬謭謮謯謰謱謲謳謴謵謶謷謸謹謺謻謼謽謾謿譀譁譂譃譄譅譆譇譈證譊譋譌譍譎譏譐譑譒譓譔譕譖譗識譙譚譛譜譝譞譟譠譡譢譣譤譥警譧譨譩譪譫譭譮譯議譱譲譳譴譵譶護譸譹譺譻譼譽譾譿讀讁讂讃讄讅讆讇讈讉變讋讌讍讎讏讐讑讒讓讔讕讖讗讘讙讚讛讜讝讞讟讠计订讣认讥讦讧讨让讪讫讬训议讯记讱讲讳讵讷讹讻讼讽读设读诂诐诒诔诖诘诙诚诜诟诣诤诨诩诪诰诳诶诶诹诺诼诽诿谀谂谄谇谉谌谑谒谔谕谖谗谘谙谝谟谠谡谪谫谮谯谰谲谳谵谶谸谹谺谻谼谽谾谿豀豊豂豃豄豅豈豍豎豏豐豑豒豓豔豖豗豘豙豛豜豝豞豟豠豣豤豥豦豧豨豩豬豭豮豯豰豱豲豴豵豶豷豻豼豽豾豿貀貁貃貄貆貇貈貋貏貐貑貒貓貕貖貗貚貛貜貝貞貟負貣貤貥貦貧財貪貫責貭貮貯貰貱貲貳貴貵貶買貸貹貺費貼貽貾貿賀賁賂賃賄賅賆資賈賉賋賌賍賎賏賐賑賒賓賔賕賖賗賘賙賚賛賜賝賟賠賡賢賣賤賥賦賧賨賩質賫賬賭賮賯賰賱賲賳賴賵賶賷賸賹賺賻賽賾賿贀贁贂贃贄贅贆贇贈贉贊贋贌贍贎贏贐贑贒贓贔贕贖贗贘贙贚贛贜贝贞负贠贡财责贤败账货质贩贪贫贬购贮贯贰贱贲贳贴贶贷贻贽赘赆赇赈赉赊赋赍赎赏赑赒赓赔赕赗赙赝赟赠赥赨赩赪赬赭赮赯赱赲赸赹赺赻赼赽赾赿趀趂趃趆趇趈趉趌趍趎趏趐趒趓趕趖趗趘趙趚趛趜趝趞趠趡趢趤趥趦趧趨趩趪趫趬趭趮趯趰趲趶趷趸趹趺趻趼趽跀跁跂跅跇跈跉跊跍跐跒跓跔跕跖跗跘跙跚跛跜跞跠跡跢跣跤跥跦跧跩跭跮跰跱跲跴跶跷跼跽跾跿踀踁踂踃踄踆踇踈踍踎踑踒踓踕踖踗踘踙踚踛踜踞踟踠踡踤踥踦踧踨踫踭踰踱踲踳踴踶踷踸踹踺踻踼踽踾踿蹃蹅蹆蹌蹍蹎蹏蹐蹑蹒蹓蹔蹕蹖蹗蹘蹚蹛蹜蹝蹞蹟蹠蹡蹢蹣蹤蹥蹧蹨蹪蹫蹮蹱蹲蹳蹵蹶蹷蹸蹹蹺蹻蹼蹽蹾蹿躀躂躃躄躆躈躉躊躋躌躍躎躑躒躓躕躖躗躘躙躚躛躝躞躟躠躡躢躣躤躥躦躧躨躩躪躭躮躰躱躳躴躵躶躷躸躹躺躻躼躽躾躿軀軁軂軃軄軅軆軇軈軉車軋軌軍軎軏軐軑軒軓軔軕軖軗軘軙軚軛軜軝軞軟軠軡転軣軤軥軦軧軨軩軪軫軬軭軮軯軰軱軲軳軴軵軶軷軸軹軺軻軼軽軾軿軿輀輁輂較輄輅輆輇輈載輊輋輌輍輎輏輐輑輒輓輔輕輖輗輘輙輚輛輜輝輞輟輠輡輢輣輤輥輦輧輨輩輪輫輬輭輮輯輰輱輲輳輴輵輶輷輸輹輺輻輼輽輾輿轀轁轂轃轄轅轆轇轈轉轊轋轌轍轎轏轐轑轒轓轔轕轖轗轘轙轚轛轜轝轞轟轠轡轢轣轤轥轪轫转轭轮轱轲轳轵轷轸轹轺轾辀辁辂较辄辇辈辋辌辎辏辐辒输辔辕辘辚辛辝辠辡辢辤辥辦辧辪辬辭辮辯農辳辴辵辸辺辻辿辿迀迃迆迉迊迋迌迍迏迒迖迗迚迠迡迣迧迬迯迱迲迴迵迶迺迻迼迾迿逇逈逌逎逓逕逘逜逖逘逜逖逤逥逧逨逩逪逫逬逭逳逴逶逷逺逻逼迾迿邁邂邃邅邆邇邉邊邋邌邍邎邏邐邒邔邖邘邚邜邞邟邠邤邥邧邨邩邫邭邲邷邼邽邾邿郀郂郃郄郅郆郈郉郋郌郍郏郐郒郓郔郕郖郘郙郚郛郜郝郞郟郠郣郤郥郩郪郬郮郰郱郲郳郵郶郷郸郹郺郻郼都郾郿鄀鄁鄃鄄鄅鄆鄇鄈鄉鄊鄋鄌鄍鄎鄏鄐鄑鄒鄓鄔鄕鄖鄗鄘鄚鄛鄜鄝鄟鄠鄡鄤鄥鄦鄧鄨鄩鄪鄫鄬鄭鄮鄰鄱鄲鄳鄴鄵鄶鄷鄸鄺鄻鄼鄽鄾鄿酀酁酂酃酄酅酆酇酈酉酊酎酏酐酑酓酔酕酖酘酙酛酜酝酞酠酡酢酣酤酥酦酧酨酩酫酭酯酰酱酲酳酴酹酺酻酼酽酾酿醀醁醂醃醄醆醈醊醎醏醐醑醓醔醕醖醗醘醙醝醠醡醤醥醦醧醨醩醫醬醭醮醯醰醱醲醳醶醷醸醹醻醼醽醾醿釀釁釂釃釄釅釆釈釉释釋里重野量釐金釒釓釔釕釖釗釘釙釚釛針釞釟釠釡釢釣釤釥釦釧釨釩釪釫釬釭釮釯釰釱釲釳釴釵釶釷釸釹釺釻釼釽釾釿鈀鈁鈂鈃鈄鈅鈆鈇鈈鈉鈊鈋鈌鈍鈎鈏鈐鈑鈒鈓鈔鈕鈖鈗鈘鈙鈚鈛鈜鈝鈞鈟鈠鈡鈢鈣鈤鈥鈦鈧鈨鈩鈪鈫鈬鈭鈮鈯鈰鈱鈲鈳鈴鈵鈶鈷鈸鈹鈺鈻鈼鈽鈾鈿鉀鉁鉂鉃鉄鉅鉆鉇鉈鉉鉊鉋鉌鉍鉎鉏鉐鉑鉒鉓鉔鉕鉖鉗鉘鉙鉚鉛鉜鉝鉞鉟鉠鉡鉢鉣鉤鉥鉦鉧鉨鉩鉪鉫鉬鉭鉮鉯鉰鉱鉲鉳鉴鉵鉶鉷鉸鉹鉺鉻鉼鉽鉾鉿銀銁銂銃銄銅銆銇銈銉銊銋銌銍銎銏銐銑銒銓銔銕銖銗銘銙銚銛銜銝銞銟銠銡銢銣銤銥銦銧銨銩銪銫銬銭銮銯銰銱銲銳銴銵銶銷銸銹銺銻銼銽銾銿鋀鋁鋂鋃鋄鋅鋆鋇鋉鋊鋋鋌鋍鋎鋏鋐鋑鋒鋓鋔鋕鋖鋗鋘鋙鋚鋛鋜鋝鋞鋟鋠鋡鋢鋣鋤鋥鋦鋧鋨鋩鋪鋫鋬鋭鋮鋯鋰鋱鋲鋳鋴鋵鋶鋷鋸鋹鋺鋻鋼鋽鋾鋿錀錁錂錃錄錅錆錇錈錉錊錋錌錍錎錏錐錑錒錓錔錕錖錗錘錙錚錛錜錝錞錟錠錡錢錣錤錥錦錧錨錩錪錫錬錭錮錯錰錱録錳錴錵錶錷錸錹錺錻錼錽錾錿鍀鍁鍂鍃鍄鍅鍆鍇鍈鍉鍊鍋鍌鍍鍎鍏鍐鍑鍒鍓鍔鍕鍖鍗鍘鍙鍚鍛鍜鍝鍞鍟鍠鍡鍢鍣鍤鍥鍦鍧鍨鍩鍪鍫鍬鍭鍮鍯鍰鍱鍲鍳鍴鍵鍶鍷鍸鍹鍺鍻鍼鍽鍾鍿鎀鎁鎂鎃鎄鎅鎆鎇鎈鎉鎊鎋鎌鎍鎎鎏鎐鎑鎒鎓鎔鎕鎖鎗鎘鎙鎚鎛鎜鎝鎞鎟鎠鎡鎢鎣鎤鎥鎦鎧鎨鎩鎪鎫鎬鎭鎮鎯鎰鎱鎲鎳鎴鎵鎶鎷鎸鎹鎺鎻鎼鎽鎾鎿鏀鏁鏂鏃鏄鏅鏆鏇鏈鏉鏋鏌鏍鏎鏏鏐鏑鏒鏓鏔鏕鏗鏘鏙鏚鏛鏜鏝鏞鏟鏠鏡鏢鏣鏤鏥鏦鏧鏨鏩鏪鏫鏬鏭鏮鏯鏰鏱鏲鏳鏴鏵鏶鏷鏸鏹鏺鏻鏼鏽鏾鏿鐀鐁鐂鐃鐄鐅鐆鐇鐈鐉鐊鐋鐌鐍鐎鐏鐐鐑鐒鐓鐔鐕鐖鐗鐘鐙鐚鐛鐜鐝鐞鐟鐠鐡鐢鐣鐤鐥鐦鐧鐨鐩鐪鐫鐬鐭鐮鐯鐰鐱鐲鐳鐴鐵鐶鐷鐸鐹鐺鐻鐼鐽鐾鐿鑀鑁鑂鑃鑄鑅鑆鑇鑈鑉鑊鑋鑌鑍鑎鑏鑐鑑鑒鑓鑔鑕鑖鑗鑘鑙鑚鑛鑜鑝鑞鑟鑠鑡鑢鑣鑤鑥鑦鑧鑨鑩鑪鑫鑬鑭鑮鑯鑰鑱鑲鑳鑴鑵鑶鑷鑸鑹鑺鑻鑼鑽鑾鑿钀钁钂钃钄钅钆钇针钉钊钋钌钍钎钏钐钑钒钓钔钕钖钘钙钚钛钜钝钞钟钡钢钣钤钥钦钧钨钩钪钫钬钭钮钯钭钲钳钴钵钶钷钸钹钺钻钼钽钾钿铀铁铇铈铉铊铋铌铍铎铏铐铑铒铕铖铗铘铙铚铛铝铞铟铡铢铣铤铥铦铧铨铩铪铫铬铯铱铳铴铵银铷铸铹铻铼铽链银铿链铫铿锂锃锄锅锆锇锈锉锊锋锎锏锐锑锒锓锔锕锖锗锘错锚锛锝锞锟锠锡锢锣锤锥锦锧锨锩锪锫锬锭键锯锰锱锲锳锴锵锶锷锸锹锺锻锼锽锾锿镀镁镂镃镄镅镆镇镈镉镊镋镌镍镎镏镐镑镒镓镔镕镖镗镘镙镚镛镜镝镞镟镠镡镢镣镤镥镦镧镨镩镪镫镬镭镮镯镰镱镲镳镴镵镶镸镹镺镻镼镽镾长門閁閂閃閄閅閆閇閈閉閊開閌閍閎閏閐閑閒間閔閕閖閗閘閙閚閛閜閝閞閟閠閡関閣閤閥閦閧閨閩閪閫閬閭閮閯閰閱閲閳閴閵閶閷閸閹閺閻閼閽閾閿闀闁闂闃闄闅闆闇闈闉闊闋闌闍闎闏闐闑闒闓闔闕闖闗闘闙闚闛關闝闞闟闠闡闢闣闤闥闦闧门闩闪闫闬闭闱闳闶闷闸闹闺闻闼闽闾闿阇阆阇阈阉阊阋阌阍阎阏阐阑阒阓阕阖阗阘阚阛阜阝阞阠阡阢阣阤阥阦阧阨阩阫阬阭阯阰阷阸阹阺阾阿陁陂陃附际陇陉陊陎陏陑陒陓陖陗')
        
        found = []
        
        # 检测连续的生僻字（3个以上）
        # 使用 Unicode 范围检测
        rare_char_sequence = []
        current_sequence = []
        
        for char in text:
            # 检查是否是生僻字
            is_rare = False
            code = ord(char)
            
            # 检查是否在生僻字范围内
            for start, end in rare_char_ranges:
                if start <= code <= end:
                    is_rare = True
                    break
            
            # 或者检查是否在已知填充字符列表中
            if char in known_filler_chars:
                is_rare = True
            
            if is_rare:
                current_sequence.append(char)
            else:
                if len(current_sequence) >= 3:
                    found.append(''.join(current_sequence))
                current_sequence = []
        
        # 处理末尾的序列
        if len(current_sequence) >= 3:
            found.append(''.join(current_sequence))
        
        return found
    
    def _ai_fix(self, text: str) -> MojibakeFixResult:
        """AI 修复乱码"""
        prompt = MOJIBAKE_FIX_PROMPT.format(text=text)
        response = self.llm.call(prompt)
        
        if not response.success:
            logger.error(f"LLM 调用失败: {response.error}")
            return MojibakeFixResult(
                original=text,
                fixed=text,
                changes=[],
                confidence=0.0,
                success=False
            )
        
        return self._parse_fix_response(response.content, text)
    
    def _ai_fix_batch(self, texts: List[str]) -> List[MojibakeFixResult]:
        """AI 批量修复"""
        text_list = "\n".join([f"[{i}] {t}" for i, t in enumerate(texts)])
        prompt = BATCH_MOJIBAKE_FIX_PROMPT.format(texts=text_list)
        response = self.llm.call(prompt)
        
        if not response.success:
            return [MojibakeFixResult(
                original=t,
                fixed=t,
                changes=[],
                confidence=0.0,
                success=False
            ) for t in texts]
        
        try:
            content = response.content.strip()
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content
                content = content.rsplit('```', 1)[0] if '```' in content else content
            
            data = json.loads(content)
            
            results = []
            for i, text in enumerate(texts):
                item = next((d for d in data if d.get('index') == i), None)
                if item:
                    results.append(MojibakeFixResult(
                        original=item.get('original', text),
                        fixed=item.get('fixed', text),
                        changes=item.get('changes', []),
                        confidence=item.get('confidence', 0.0),
                        success=True
                    ))
                else:
                    results.append(MojibakeFixResult(
                        original=text,
                        fixed=text,
                        changes=[],
                        confidence=0.0,
                        success=False
                    ))
            
            return results
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            return [MojibakeFixResult(
                original=t,
                fixed=t,
                changes=[],
                confidence=0.0,
                success=False
            ) for t in texts]
    
    def _parse_fix_response(self, content: str, original: str) -> MojibakeFixResult:
        """解析修复响应"""
        try:
            content = content.strip()
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content
                content = content.rsplit('```', 1)[0] if '```' in content else content
            
            data = json.loads(content)
            
            return MojibakeFixResult(
                original=data.get('original', original),
                fixed=data.get('fixed', original),
                changes=data.get('changes', []),
                confidence=data.get('confidence', 0.0),
                success=True
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}\n内容: {content[:200]}")
            return MojibakeFixResult(
                original=original,
                fixed=original,
                changes=[],
                confidence=0.0,
                success=False
            )
    
    def _learn_from_fix(self, result: MojibakeFixResult) -> None:
        """从修复结果中学习新规则"""
        for change in result.changes:
            before = change.get('before', '')
            after = change.get('after', '')
            
            if before and len(before) <= 10:  # 只学习短模式
                if before not in self.learned_rules:
                    self.learned_rules[before] = after
                    logger.info(f"学习新规则: '{before}' -> '{after}'")
        
        # 保存规则
        self._save_learned_rules()
    
    def _load_learned_rules(self) -> None:
        """加载学习到的规则"""
        rules_file = os.path.join(os.path.dirname(__file__), '..', '..', 'references', 'learned_mojibake_rules.json')
        try:
            if os.path.exists(rules_file):
                with open(rules_file, 'r', encoding='utf-8') as f:
                    self.learned_rules = json.load(f)
                logger.info(f"加载学习规则: {len(self.learned_rules)} 条")
        except Exception as e:
            logger.warning(f"加载学习规则失败: {e}")
    
    def _save_learned_rules(self) -> None:
        """保存学习到的规则"""
        rules_file = os.path.join(os.path.dirname(__file__), '..', '..', 'references', 'learned_mojibake_rules.json')
        try:
            os.makedirs(os.path.dirname(rules_file), exist_ok=True)
            with open(rules_file, 'w', encoding='utf-8') as f:
                json.dump(self.learned_rules, f, ensure_ascii=False, indent=2)
            logger.info(f"保存学习规则: {len(self.learned_rules)} 条")
        except Exception as e:
            logger.warning(f"保存学习规则失败: {e}")
    
    def stats(self) -> Dict:
        """获取统计信息"""
        return {
            'enabled': self.enabled,
            'total_processed': self.total_processed,
            'fixed_count': self.fixed_count,
            'learned_rules': len(self.learned_rules),
            'auto_learn': self.auto_learn
        }


def apply_fixes_to_text(text: str, result: MojibakeFixResult) -> Tuple[str, Dict]:
    """应用修复结果到文本"""
    stats = {
        'total_changes': len(result.changes),
        'confidence': result.confidence,
        'success': result.success
    }
    
    return result.fixed, stats
