# -*- coding: utf-8 -*-
"""更新 about 页面：去掉 creator.desc、重写免责声明、加 JavaFX 26 已知问题说明"""
import io

BASE = r'src/main/resources/i18n'

LINE11 = {
    'zh': '免责声明：本软件按「现状」提供，不附带任何明示或暗示的担保。在任何情况下，作者均不对因使用或无法使用本软件而产生的任何损害承担责任，包括但不限于：数据丢失或损坏、利润损失、业务中断、声誉受损等直接或间接损失；用户利用本软件从事违法犯罪或侵权行为所产生的一切责任与后果；对任何第三方造成的侵害；以及因软件缺陷、错误、遗漏、与第三方服务的兼容性问题或交互所引发的任何损害。此外，本软件输出的内容（含 AI 生成内容）仅供参考，不构成法律、医疗、财务等任何专业建议。',
    'zh_tw': '免責聲明：本軟體按「現狀」提供，不附帶任何明示或暗示的擔保。在任何情況下，作者均不對因使用或無法使用本軟體而產生的任何損害承擔責任，包括但不限於：資料遺失或損壞、利潤損失、業務中斷、聲譽受損等直接或間接損失；使用者利用本軟體從事違法犯罪或侵權行為所產生的一切責任與後果；對任何第三方造成的侵害；以及因軟體缺陷、錯誤、遺漏、與第三方服務的相容性問題或互動所引發的任何損害。此外，本軟體輸出的內容（含 AI 生成內容）僅供參考，不構成法律、醫療、財務等任何專業建議。',
    'en': 'Disclaimer: This software is provided "as is", without warranty of any kind. In no event shall the author be liable for any damages arising from the use or inability to use this software, including but not limited to: data loss or corruption, loss of profits, business interruption, or damage to reputation; all liability for any illegal, criminal, or infringing conduct performed by users with this software; any harm caused to third parties; and any damage caused by software defects, errors, omissions, compatibility issues, or interaction with third-party services. Furthermore, the output of this software (including AI-generated content) is for reference only and does not constitute legal, medical, financial, or any other professional advice.',
    'ja': '免責事項：本ソフトウェアは「現状のまま」提供され、いかなる種類の保証も付帯しません。著者は、本ソフトウェアの使用または使用不能に起因する如何なる損害についても責任を負いません。これには、データの喪失・破損、利益の喪失、業務の中断、評判の毀損等の直接的・間接的な損害；ユーザーが本ソフトウェアを利用して行った違法行為、犯罪行為、権利侵害に関する一切の責任と結果；第三者への如何なる侵害；ならびにソフトウェアの欠陥、エラー、欠落、第三者サービスとの互換性の問題や連携に起因する損害が含まれます。さらに、本ソフトウェアの出力（AI 生成コンテンツを含む）は参考情報であり、法的・医療・財務などの専門的助言を構成するものではありません。',
    'ko': '면책 조항：본 소프트웨어는「있는 그대로」제공되며 어떠한 종류의 보증도 포함되지 않습니다. 본 소프트웨어의 사용 또는 사용 불가로 인한 어떠한 손해에 대해서도 저작자는 책임을 지지 않습니다. 여기에는 데이터 손실·손상, 이익 손실, 업무 중단, 평판 손상 등 직접적·간접적 손해; 사용자가 본 소프트웨어를 이용하여 행한 불법·범죄·권리 침해 행위의 모든 책임과 결과; 제3자에 대한 어떠한 침해; 그리고 소프트웨어의 결함, 오류, 누락, 제3자 서비스와의 호환성 문제 또는 상호 작용으로 인한 손해가 포함됩니다. 또한 본 소프트웨어의 출력(인공지능 생성 내용 포함)은 참고용이며 법률·의료·재정 등 전문적 조언을 구성하지 않습니다.',
    'fr': 'Avertissement : ce logiciel est fourni « tel quel », sans garantie d\'aucune sorte. En aucun cas l\'auteur ne saurait être tenu responsable des dommages résultant de l\'utilisation ou de l\'impossibilité d\'utiliser ce logiciel, y compris, à titre indicatif : la perte ou corruption de données, la perte de profits, l\'interruption d\'activité, l\'atteinte à la réputation ou tout autre préjudice direct ou indirect ; la responsabilité de tout acte illégal, criminel ou contrefaisant commis par l\'utilisateur ; tout préjudice causé à des tiers ; ainsi que tout dommage résultant de défauts, erreurs, omissions, incompatibilités ou interactions avec des services tiers. En outre, les sorties de ce logiciel (y compris le contenu généré par IA) sont fournies à titre indicatif uniquement et ne constituent pas un conseil juridique, médical, financier ou de toute autre nature professionnelle.',
    'de': 'Haftungsausschluss: Diese Software wird „wie besehen" ohne jegliche Art von Garantie bereitgestellt. In keinem Fall haftet der Autor für Schäden, die aus der Nutzung oder Nichtnutzung dieser Software entstehen, einschließlich, aber nicht beschränkt auf: Datenverlust oder -beschädigung, Gewinnverlust, Geschäftsunterbrechung, Rufschädigung oder jeden anderen direkten oder indirekten Schaden; die Verantwortung für rechtswidrige, kriminelle oder rechtsverletzende Handlungen des Benutzers; jegliche Schädigung Dritter; sowie Schäden durch Softwarefehler, -mängel, -auslassungen, Kompatibilitätsprobleme oder Interaktionen mit Diensten Dritter. Darüber hinaus dienen die Ausgaben dieser Software (einschließlich KI-generierter Inhalte) nur als Referenz und stellen keine Rechts-, Medizin-, Finanz- oder sonstige professionelle Beratung dar.',
    'es': 'Aviso: este software se proporcione «tal cual», sin garantía de ningún tipo. En ningún caso será responsable el autor de los daños derivados del uso o la imposibilidad de uso de este software, incluyendo, a título enunciativo: pérdida o corrupción de datos, pérdida de beneficios, interrupción del negocio, daño a la reputación o cualquier otro perjuicio directo o indirecto; la responsabilidad por cualquier conducta ilegal, delictiva o infractora del usuario; cualquier perjuicio causado a terceros; y cualquier daño causado por defectos, errores, omisiones, incompatibilidades o interacciones con servicios de terceros. Además, las salidas de este software (incluido el contenido generado por IA) son solo de referencia y no constituyen asesoramiento legal, médico, financiero ni de ninguna otra índole profesional.',
    'pt': 'Aviso: este software é fornecido «como está», sem garantia de qualquer tipo. Em nenhum caso o autor será responsável por danos decorrentes do uso ou da impossibilidade de uso deste software, incluindo, a título exemplificativo: perda ou corrupção de dados, perda de lucros, interrupção de negócios, danos à reputação ou qualquer outro prejuízo direto ou indireto; a responsabilidade por qualquer conduta ilegal, criminosa ou infratora do usuário; qualquer dano causado a terceiros; e qualquer dano causado por defeitos, erros, omissões, incompatibilidades ou interações com serviços de terceiros. Além disso, as saídas deste software (incluindo conteúdo gerado por IA) são apenas para referência e não constituem aconselhamento jurídico, financeiro, médico ou de qualquer outra natureza profissional.',
}

LINE12 = {
    'zh': '使用本软件即表示您已阅读并同意上述全部条款。',
    'zh_tw': '使用本軟體即表示您已閱讀並同意上述全部條款。',
    'en': 'By using this software, you acknowledge that you have read and agree to all the above terms.',
    'ja': '本ソフトウェアの使用をもって、上記のすべての条項を確認し同意したものとみなされます。',
    'ko': '본 소프트웨어를 사용함으로써 위의 모든 조항을 확인하고 동의한 것으로 간주됩니다.',
    'fr': 'En utilisant ce logiciel, vous reconnaissez avoir lu et accepté l\'ensemble des présentes conditions.',
    'de': 'Durch die Nutzung dieser Software bestätigen Sie, dass Sie alle vorstehenden Bedingungen gelesen und akzeptiert haben.',
    'es': 'Al usar este software, usted reconoce haber leído y aceptado todos los términos anteriores.',
    'pt': 'Ao usar este software, você reconhece que leu e aceitou todos os termos acima.',
}

BUGS1 = {
    'zh': '输入法候选框不跟随光标位置（JavaFX 26 已知问题，Windows 中文输入法）',
    'zh_tw': '輸入法候選框不跟隨光標位置（JavaFX 26 已知問題，Windows 中文輸入法）',
    'en': 'IME candidate window does not follow the cursor (Known issue in JavaFX 26, Windows Chinese IME)',
    'ja': 'IME 変換候補がカーソルに追従しない（JavaFX 26 の既知の問題、Windows 日本語/中国語 IME）',
    'ko': '입력기 후보창이 커서 위치를 따라가지 않음 (JavaFX 26 알려진 문제, Windows 중국어 입력기)',
    'fr': 'La fenêtre de candidats IME ne suit pas le cursor (Problème connu dans JavaFX 26, IME chinois Windows)',
    'de': 'IME-Kandidatenfenster folgt nicht dem Cursor (Bekanntes Problem in JavaFX 26, Windows-Chinesisch-IME)',
    'es': 'La ventana de candidatos IME no sigue al cursor (Problema conocido en JavaFX 26, IME chino de Windows)',
    'pt': 'A janela de candidatos do IME não segue o cursor (Problema conhecido no JavaFX 26, IME chinês do Windows)',
}

LANGS = ['zh', 'zh_tw', 'en', 'ja', 'ko', 'fr', 'de', 'es', 'pt']

def main():
    for lang in LANGS:
        p = '%s\\texts_%s.properties' % (BASE, lang)
        lines = io.open(p, encoding='utf-8').read().splitlines()
        out = []
        seen = set()
        for line in lines:
            if line and not line.startswith('#') and '=' in line:
                k = line.split('=', 1)[0].strip()
                if k in seen:
                    continue
                seen.add(k)
                if k == 'about.creator.desc':
                    continue  # 删除此行
                if k == 'about.license.line11':
                    out.append(k + '=' + LINE11[lang])
                    continue
                if k == 'about.license.line12':
                    out.append(k + '=' + LINE12[lang])
                    continue
                if k == 'about.bugs.line1':
                    out.append(k + '=' + BUGS1[lang])
                    continue
            out.append(line)
        io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        print('%s updated' % lang)

if __name__ == '__main__':
    main()
