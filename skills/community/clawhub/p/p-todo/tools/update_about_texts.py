# -*- coding: utf-8 -*-
"""更新 9 个语言文件的关于页内容：版本去 alpha、制作人、署名、免责声明完善"""
import io

BASE = r'src/main/resources/i18n'

# key -> {lang: 新值}
UPDATES = {
    'about.version': {
        'zh': 'v1.0.0', 'zh_tw': 'v1.0.0', 'en': 'v1.0.0', 'ja': 'v1.0.0',
        'ko': 'v1.0.0', 'fr': 'v1.0.0', 'de': 'v1.0.0', 'es': 'v1.0.0', 'pt': 'v1.0.0',
    },
    'about.creator.tech': {
        'zh': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'zh_tw': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'en': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'ja': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'ko': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'fr': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'de': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'es': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
        'pt': '+MiMo-v2.5-pro + Qwen3.8-27b + DeepSeek-v4-pro/flash',
    },
    'about.creator.desc': {
        'zh': '专注于桌面效率工具。',
        'zh_tw': '專注於桌面效率工具。',
        'en': 'Focused on desktop productivity tools.',
        'ja': 'デスクトップ生産性ツールに特化しています。',
        'ko': '데스크톱 생산성 도구에 집중하고 있습니다.',
        'fr': 'Axé sur les outils de productivité de bureau.',
        'de': 'Fokussiert auf Desktop-Produktivitätstools.',
        'es': 'Centrado en herramientas de productividad de escritorio.',
        'pt': 'Focado em ferramentas de produtividade para desktop.',
    },
    'about.license.line10': {
        'zh': '  • 如果是整体项目由此改造，请在关于页面或文档中注明「基于 Pondsi 的代码 改造」',
        'zh_tw': '  • 如果是整體項目由此改造，請在關於頁面或文檔中註明「基於 Pondsi 的程式碼 改造」',
        'en': '  • If the whole project is derived from this one, note "Based on Pondsi\'s code" on the About page or in the documentation',
        'ja': '  • プロジェクト全体が本ソフトから派生した場合は、情報ページ等に「Pondsi のコードをベースに改変」と明記すること',
        'ko': '  • 전체 프로젝트가 본 소프트웨어에서 파생된 경우 정보 페이지나 문서에「Pondsi의 코드를 기반으로 개작」을 명시해야 합니다',
        'fr': '  • Si le projet entier est dérivé de celui-ci, mentionnez « Basé sur le code de Pondsi » dans la page À propos ou la documentation',
        'de': '  • Bei einem vollständig abgeleiteten Projekt „Basiert auf Pondsis Code" auf der Über-Seite oder in der Dokumentation vermerken',
        'es': '  • Si todo el proyecto deriva de este, indica «Basado en el código de Pondsi» en la página Acerca de o en la documentación',
        'pt': '  • Se o projeto inteiro for derivado deste, indique «Baseado no código do Pondsi» na página Sobre ou na documentação',
    },
    'about.license.line11': {
        'zh': '免责声明：本软件按「现状」提供，不作任何明示或暗示的担保。作者不对因使用或无法使用本软件而产生的任何直接、间接、偶然、特殊或后果性损害承担责任，包括但不限于：数据丢失或损坏、利润损失、业务中断、声誉受损；用户利用本软件从事的任何违法、犯罪、侵权或不当行为，其全部责任与后果由用户自行承担；对任何第三方造成的任何侵害；因软件缺陷、错误、遗漏、兼容性问题或与第三方服务交互而引发的任何损害。本软件输出内容（含 AI 生成内容）仅供参考，不构成法律、医疗、财务等专业建议。',
        'zh_tw': '免責聲明：本軟體按「現狀」提供，不作任何明示或暗示的擔保。作者不對因使用或無法使用本軟體而產生的任何直接、間接、偶然、特殊或後果性損害承擔責任，包括但不限於：資料遺失或損壞、利潤損失、業務中斷、聲譽受損；使用者利用本軟體從事的任何違法、犯罪、侵權或不當行為，其全部責任與後果由使用者自行承擔；對任何第三方造成的任何侵害；因軟體缺陷、錯誤、遺漏、相容性問題或與第三方服務互動而引發的任何損害。本軟體輸出內容（含 AI 生成內容）僅供參考，不構成法律、醫療、財務等專業建議。',
        'en': 'Disclaimer: This software is provided "as is", without warranty of any kind, express or implied. The author shall not be liable for any direct, indirect, incidental, special or consequential damages arising from the use or inability to use this software, including but not limited to: data loss or corruption, loss of profits, business interruption, damage to reputation; all responsibility and consequences of any illegal, criminal, infringing or improper conduct performed by users with this software shall be borne solely by the users themselves; any harm caused to any third party; and any damage caused by software defects, errors, omissions, compatibility issues or interaction with third-party services. The output of this software (including AI-generated content) is for reference only and does not constitute legal, medical, financial or any other professional advice.',
        'ja': '免責事項：本ソフトウェアは「現状有姿」で提供され、明示・黙示を問わずいかなる保証もありません。著作者は、本ソフトウェアの使用または使用不能に起因する直接的、間接的、偶発的、特別または結果的な損害について一切責任を負いません。これには、データの喪失・破損、利益の喪失、業務の中断、評判の毀損が含まれますがこれらに限りません。ユーザーが本ソフトウェアを利用して行った違法行為、犯罪行為、権利侵害または不適切な行為のすべての責任と結果は、ユーザー自身が負うものとします。第三者に対するいかなる侵害、ならびにソフトウェアの欠陥、エラー、欠落、互換性の問題、または第三者サービスの連携に起因する損害についても同様です。本ソフトウェアの出力（AI 生成コンテンツを含む）は参考用であり、法的・医療・財務などの専門的助言を構成するものではありません。',
        'ko': '면책 조항：본 소프트웨어는「있는 그대로」제공되며 명시적이든 묵시적이든 어떠한 보증도 하지 않습니다. 저작자는 본 소프트웨어의 사용 또는 사용 불가로 인한 직접적, 간접적, 우연적, 특별 또는 결과적 손해에 대해 책임을 지지 않습니다. 여기에는 데이터 손실·손상, 이익 손실, 업무 중단, 평판 손상이 포함되지만 이에 국한되지 않습니다. 사용자가 본 소프트웨어를 이용하여 행한 불법 행위, 범죄 행위, 권리 침해 또는 부적절한 행위의 모든 책임과 결과는 사용자 본인이 부담합니다. 제3자에 대한 어떠한 침해, 그리고 소프트웨어의 결함, 오류, 누락, 호환성 문제 또는 제3자 서비스와의 상호 작용으로 인한 손해도 마찬가지입니다. 본 소프트웨어의 출력(인공지능 생성 내용 포함)은 참고용이며 법률, 의료, 재정 등 전문적 조언을 구성하지 않습니다.',
        'fr': 'Avertissement : ce logiciel est fourni « tel quel », sans garantie d\'aucune sorte, expresse ou implicite. L\'auteur décline toute responsabilité pour les dommages directs, indirects, accessoires, spéciaux ou consécutifs résultant de l\'utilisation ou de l\'impossibilité d\'utiliser ce logiciel, y compris, sans s\'y limiter : perte ou corruption de données, perte de profits, interruption d\'activité, atteinte à la réputation ; toute responsabilité et conséquence d\'actes illégaux, criminels, contrefaisants ou inappropriés commis par l\'utilisateur avec ce logiciel relèvent uniquement de l\'utilisateur ; tout préjudice causé à un tiers ; ainsi que tout dommage résultant de défauts, erreurs, omissions, problèmes de compatibilité ou interactions avec des services tiers. Les sorties de ce logiciel (y compris le contenu généré par IA) sont fournies à titre de référence uniquement et ne constituent pas des conseils juridiques, médicaux, financiers ou professionnels.',
        'de': 'Haftungsausschluss: Diese Software wird „wie besehen" ohne jegliche ausdrückliche oder stillschweigende Garantie bereitgestellt. Der Autor haftet nicht für direkte, indirekte, zufällige, besondere oder Folgeschäden, die aus der Nutzung oder Nichtnutzung dieser Software entstehen, einschließlich, aber nicht beschränkt auf: Datenverlust oder -beschädigung, Gewinnverlust, Geschäftsunterbrechung, Rufschädigung; alle Verantwortung und Folgen illegaler, krimineller, rechtsverletzender oder unangemessener Handlungen, die Benutzer mit dieser Software durchführen, liegen allein beim Benutzer; jegliche Schädigung Dritter; sowie Schäden durch Softwarefehler, -mängel, -auslassungen, Kompatibilitätsprobleme oder die Interaktion mit Diensten Dritter. Die Ausgaben dieser Software (einschließlich KI-generierter Inhalte) dienen nur zur Referenz und stellen keine Rechts-, Medizin- oder Finanzberatung dar.',
        'es': 'Aviso: este software se proporciona «tal cual», sin garantía de ningún tipo, expresa o implícita. El autor no se hace responsable de los daños directos, indirectos, incidentales, especiales o consecuentes derivados del uso o la imposibilidad de uso de este software, incluidos, entre otros: pérdida o corrupción de datos, pérdida de beneficios, interrupción del negocio, daño a la reputación; toda responsabilidad y consecuencia de actos ilegales, delictivos, infractores o inapropiados realizados por el usuario con este software recae únicamente en el usuario; cualquier perjuicio causado a terceros; así como cualquier daño causado por defectos, errores, omisiones, problemas de compatibilidad o interacción con servicios de terceros. Las salidas de este software (incluido el contenido generado por IA) son solo de referencia y no constituyen asesoramiento legal, médico, financiero ni profesional.',
        'pt': 'Aviso: este software é fornecido «como está», sem garantia de qualquer tipo, expressa ou implícita. O autor não se responsabiliza por danos diretos, indiretos, incidentais, especiais ou consequentes decorrentes do uso ou da impossibilidade de uso deste software, incluindo, entre outros: perda ou corrupção de dados, perda de lucros, interrupção de negócios, danos à reputação; toda responsabilidade e consequência de atos ilegais, criminosos, infratores ou inadequados realizados pelo usuário com este software recaem exclusivamente sobre o usuário; qualquer dano causado a terceiros; bem como qualquer dano causado por defeitos, erros, omissões, problemas de compatibilidade ou interação com serviços de terceiros. As saídas deste software (incluindo conteúdo gerado por IA) são apenas para referência e não constituem aconselhamento jurídico, médico, financeiro ou profissional.',
    },
    'about.license.line12': {
        'zh': '使用本软件即表示您已知悉并同意承担全部风险并接受本免责声明。',
        'zh_tw': '使用本軟體即表示您已知悉並同意承擔全部風險並接受本免責聲明。',
        'en': 'By using this software, you acknowledge that you have read and agree to assume all risks and accept this disclaimer.',
        'ja': '本ソフトウェアの使用をもって、すべてのリスクを理解し同意し、本免責事項を受け入れたものとみなされます。',
        'ko': '본 소프트웨어를 사용함으로써 모든 위험을 이해하고 동의하며 본 면책 조항을 수락한 것으로 간주됩니다.',
        'fr': 'En utilisant ce logiciel, vous reconnaissez avoir pris connaissance des risques et acceptez cette clause de non-responsabilité.',
        'de': 'Mit der Nutzung dieser Software erkennen Sie an, alle Risiken verstanden zu haben, und akzeptieren diesen Haftungsausschluss.',
        'es': 'Al usar este software, usted reconoce haber comprendido todos los riesgos y acepta esta cláusula de exención de responsabilidad.',
        'pt': 'Ao usar este software, você reconhece que compreendeu todos os riscos e aceita esta isenção de responsabilidade.',
    },
    'about.progress.line1': {
        'zh': '当前版本：v1.0.0（内测版）',
        'zh_tw': '目前版本：v1.0.0（內測版）',
        'en': 'Current version: v1.0.0 (beta)',
        'ja': '現在のバージョン：v1.0.0（ベータ版）',
        'ko': '현재 버전：v1.0.0（베타）',
        'fr': 'Version actuelle : v1.0.0 (bêta)',
        'de': 'Aktuelle Version: v1.0.0 (Beta)',
        'es': 'Versión actual: v1.0.0 (beta)',
        'pt': 'Versão atual: v1.0.0 (beta)',
    },
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
                if k in UPDATES:
                    if k in seen:
                        continue  # 重复 key 跳过（保留已输出的新值）
                    seen.add(k)
                    out.append(k + '=' + UPDATES[k][lang])
                    continue
            out.append(line)
        io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        print('%s updated' % lang)

if __name__ == '__main__':
    main()
