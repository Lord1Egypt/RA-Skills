#!/usr/bin/env python3
"""
LaTeX Template Generator for Academic Papers
Generates complete LaTeX templates compliant with various journal/conference formats.

Supported venues:
- IEEE (Transactions, Journals)
- ACM (ToIS, CCS, etc.)  
- NeurIPS/ICLR (Conference formats)
- Custom template support

Usage:
    python generate_latex_template.py --journal "IEEE TIFS" --output draft_initial.tex
"""

import argparse
from datetime import datetime
from pathlib import Path


class LaTeXTemplateGenerator:
    """Generate LaTeX templates for academic paper writing."""
    
    JOURNAL_TEMPLATES = {
        "ieee_transaction": {
            "package": "IEEEtran",
            "layout": "two column",
            "font_size": "10pt",
            "template_type": "@article"
        },
        "acm_transaction": {
            "package": "ACM-Trans",
            "layout": "two column", 
            "font_size": "10pt",
            "template_type": "@article"
        },
        "neurips": {
            "package": "nips_2023",
            "layout": "two column doubleblind",
            "font_size": "10pt",  
            "template_type": "@inproceedings"
        }
    }
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_full_template(self, journal_name: str, paper_title: str, 
                             authors: List[str]) -> str:
        """Generate complete LaTeX template with all standard sections."""
        
        template_config = None
        for key, config in self.JOURNAL_TEMPLATES.items():
            if key.lower() in journal_name.lower():
                template_config = config
                break
                
        # Fallback to generic IEEE format if not found
        if template_config is None:
            template_config = self.JOURNAL_TEMPLATES["ieee_transaction"]
            
        latex_content = f"""% {{paper_title}} - PhD Research Paper Draft
% Generated: {datetime.now().isoformat()}  
% Journal Target: {journal_name}

\\documentclass[acm]{template_config['package']}  % or change to IEEEtran/ACM-Trans/other

\\usepackage{{amsmath}}    % Math symbols and environments
\\usepackage{{amssymb}}     % Extended math symbols  
\\usepackage{{amsfonts}}    % Math fonts
\\usepackage{{graphicx}}    % Include figures
\\usepackage{{booktabs}}    % Professional tables
\\usepackage{{algorithm}}   % Algorithms
\\usepackage{{algpseudocode}} % Pseudocode formatting
\\usepackage{{hyperref}}    % Hyperlinks
\\usepackage{{cite}}        % Citation handling

% Paper metadata
\\title{{{paper_title}}}  
\\author{chr(10).join("  {}\\and\n".join([f"{a.strip()} \\thanks{{Affiliation/University}}" for a in authors]))}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
\\noindent 
% Write your abstract here - typically 150-250 words summarizing the main contributions, methods, and results.
Abstract content will be developed based on final paper structure.

\\keywords{Your keywords here}

\\end{{abstract}}


% ============================================================
SECTION I: INTRODUCTION
============================================================ \\section{Introduction}

This section should introduce your research problem with proper motivation.

\\subsubsection{Research Motivation}

Include 2-3 paragraphs covering:
\\begin{{itemize}}
\\\\item Real-world significance of the problem  
\\\\item Legal/commercial/technical drivers
\\\\item Gap in existing solutions
\\\\item Your proposed approach overview
\\\\end{{itemize}}

\\subsubsection{Main Contributions}

Summarize your 3-4 core research contributions:
\\begin{{enumerate}} 
\\\\item \\textbf{[Contribution 1]}: Novel algorithm/method framework...
\\\\item \\textbf{[Contribution 2]}: Theoretical analysis with guarantees...
\\\\item \\textbf{[Contribution 3]}: Empirical validation across multiple datasets...  
\\\\end{{enumerate}}

\\subsubsection{Paper Organization} 

\\paragraph{Outline:} Section II surveys related work. Section III presents our methodology with formal proofs. 
Section IV details experimental setup and results analysis. 
Section V discusses limitations and future directions.  

\\noindent
\\textit{TODO: Complete this section with detailed motivation statements from your research narrative.}\\

% ============================================================  
SECTION II: RELATED WORK
============================================================ \\section{Related Work}

Systematically review existing literature, organizing by methodology paradigm rather than chronologically.

\\subsection{Background and Problem Context}

Provide necessary background for readers unfamiliar with the domain:

\\begin{{theorem}}[Fundamental Notation]\\textbf{(Placeholder Theorem 1)}
% Define core notation here
Let $math$ represent your model architecture... 
\\end{{theorem}}  

\\noindent \\textit{TODO: Formalize all notation used throughout the paper. Include symbol table in Appendix.}

\\\\subsection{Machine Unlearning Approaches [if applicable]}  
Review key works in your primary research thread, such as:

\\begin{{itemize}}
\\\\item Forgetting through retraining-based methods [Citation]
\\\\item Certificate-based verifiable unlearning [Citation] 
\\\\item Differential privacy approaches (with distinction from certified) [Citation]
\\\\end{{itemize}}  

\\subsection{[Secondary Thread Title Here]}

% Describe related or alternative methodological paradigms.  
% Explain why existing solutions are insufficient for your use case.  

\\noindent \\textit{TODO: Expand with citations from your literature survey results.}\\


% ============================================================
SECTION III: METHODOLOGY  
============================================================ % This is where your core innovation lives

\\section{Methodology}

Our proposed approach comprises the following components:

\\\\subsection{Problem Formulation}

Formally define the research problem:

\\begin{{definition}}[Unlearning Task]  % Customize theorem name
Given a model $M$ trained on dataset $D = {{(x_i, y_i)}}$, and an unlearning request for subset $D_f \subset D$, 
the goal is to produce updated model $M'$ such that...
\\end{{definition}}  

% Add your formal definitions here

\\\\subsection{Core Algorithm}

Present your main approach with mathematical rigor:

\\begin{{algorithm}}[H]
\\caption{Proposed Unlearning Framework}  
\\begin{{algorithmic}}{{1}} 
\\\\STATE \\textbf{Input}: Model $M$, dataset $D$, forget subset $D_f$
\\\\STATE \\textbf{Output}: Updated model $M'$ with verified unlearning guarantee

\\\\STATE Step 1: Identify affected data structures
\\\\IF {{condition met}}
\\\\STATE Apply parameter update rule from Theorem~\\ref{{thm:main_theorem}}
\\\\ELSE  
\\\\STATE Use alternative procedure outlined in Section III-C
\\\\ENDIF 

\\\\STATE Step 2: Verify unlearning effectiveness (Section IV metrics)  
\\\\STATE Return updated model $M'$ with certificate

\\end{{algorithmic}}  
\\end{{algorithm}}  

\\subsection{Theoretical Analysis}

Provide formal proofs establishing correctness and guarantees.

\\begin{{theorem}}[Main Guarantees]\\textbf{(Theorem 3)}
Under Assumptions 1-2, our approach provides $epsilon$-bounded update to full retraining...  
\\end{{theorem}}  

\noindent \\textbf{Proof Sketch:}  
Start with initial conditions and bound gradient updates. Full proof in Appendix A.

\\noindent \\textit{TODO: Add complete formal statements + proofs of all key claims. Verify math proof consistency before submission.}\\


% ============================================================
SECTION IV: EXPERIMENTS  
============================================================ % Empirical validation section

\\section{Experimental Setup and Results}  

Comprehensive empirical verification:

\\\\subsection{Datasets and Implementation Details}

\\textbf{Datasets Used}:  
\\begin{{itemize}}  
\\\\item CIFAR-10 (standard benchmark for classification)
\\\\item Fashion-MNIST (alternative distribution test)  
\\\\item Custom dataset B domain-specific validation)
\\\\end{{itemize}}  

\\textbf{Implementation}:  
Model architectures, hyperparameters, training protocols.

\\\\subsection{Baseline Comparison Methods}  
Evaluate against established baselines:

% Insert comparison table here  
\\begin{{table}}[h] 
\\centering  
\\caption{Comparison with Baseline Methods Across Datasets}
\\label{{tab:baseline_comparison}}  
\\begin{{tabular}}{{lcccc}}    
\\\\toprule 
Method & CIFAR-10 Acc. (\%) & Runtime (s) & Unlearning Efficiency & Privacy Guarantee \\\\  
\\\\midrule  
NAU [23] & 85.4 & 342.7 & Baseline & None \\\\  
SISA [20] & 84.9 & 120.5 & High & Partial \\\\  
\\textbf{Ours} & \\textbf{{88.2}} & \\textbf{{185.3}} & \\textbf{{High}} & \\textbf{{Certified}} \\\\  
\\\\bottomrule  
\\end{{tabular}}
\\end{{table}}  

\\\\subsection{Ablation Study Results}

% Validate individual component contributions:

\\begin{{itemize}}
\\\\item Remove Component A → Performance drops 3.5% → Critical function identified
\\\\item Remove Component B → Minimal impact (<0.5%) → Redundancy detected  
\\\\item Combined effect shows synergy between components  
\\\\end{{itemize}}  

\\subsection{Robustness Analysis}

Test against adversarial examples, distribution shifts, etc.


% ============================================================
SECTION V: DISCUSSION AND LIMITATIONS  
============================================================ % Honest assessment of your work scope

\\section{Discussion and Limitations}  

Be explicit about what your method cannot do - strengthens credibility.

\\\\subsection{Practical Implications}

Discuss how your findings impact practitioners in the field.

\\\\subsection{Recognized Limitations}  

\\begin{{itemize}} 
\\\\item Scalability constraints for very large models...  
\\\\item Assumptions that may not hold in all real-world scenarios...
\\\\item Dataset bias considerations...
\\\\end{{itemize}}  

\\\\subsection{Future Work Directions}

Outline next steps and potential extensions based on current work.


% ============================================================
SECTION VI: CONCLUSION  
============================================================ % Brief summary and impact statement

\\section{Conclusion} 

Summarize main findings and emphasize the research contributions. Reiterate why this matters for the field.  

% ============================================================
REFERENCES  
============================================================ \bibliographystyle{{plain}}  
\\bibliography{{references}}  % Your .bib file here


% ============================================================
APPENDICES (Supplementary Material)  
============================================================ % Optional but recommended for long proofs, extended analysis

\\appendix

\\section{Extended Proofs}  
Full mathematical derivations and lemma statements.

\\\\section{Additional Experimental Results}
Tables, plots not included in main text due to space constraints.

% =============================================================
SYMBOL NOTATION TABLE  
=========================================================== \section{Notation Reference Guide}

\\begin{{tabular}}{{lll}} 
\\\\toprule 
Symbol & Definition & Section First Used \\\\
\\\\midrule  
$M$ & Model parameters & III-A \\\\  
$D$ & Training dataset & II-C \\\\  
$epsilon$ & Privacy budget parameter & III-D \\\\  
\\\\bottomrule  
\\end{{tabular}}  

\\end{{document}}
"""

        return latex_content
    
    def save_template(self, content: str, filename: str):
        """Save the generated LaTeX template."""
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:  
            f.write(content)
            
        print(f"✅ Generated LaTeX template: {output_path}")
        
        # Generate companion files list
        required_files = [
            "references.bib",              # BibTeX citation file  
            "figures/*.pdf/*.eps",         # Vector graphics for figures
            "data/*.csv"                   # Additional data plots/tables if needed
        ]
        
        checklist_path = self.output_dir / "template-requirements.md" 
        with open(checklist_path, 'w') as f:
            f.write(f"# Required Companion Files\n\nGenerated Template: {filename}\n\n## To Compile Successfully:\n")
            for req in required_files:
                f.write(f"- [ ] `{req}` (placeholder until you add content)\n")
                
        print(f"✅ Created companion file checklist: {checklist_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate LaTeX template for academic paper writing with journal compliance"
    )
    
    parser.add_argument("--journal", "-j", required=True,
                       help="Target journal or conference (e.g., 'IEEE TIFS', 'ACM ToIS', 'NeurIPS')")
    parser.add_argument("--title", "-t", default="Your Paper Title Here",
                       help="Paper title for the template")
    parser.add_argument("--authors", "-a", nargs="+", default=["Author One", "Author Two"], 
                       help="List of author names (space-separated)")
    parser.add_argument("--output-dir", "-o", type=str,
                       default=None,
                       help="Output directory for LaTeX files")
    
    args = parser.parse_args()
    
    # Setup output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
        output_dir = Path(f"latex-template-{timestamp}")
        
    generator = LaTeXTemplateGenerator(output_dir)
    
    # Generate full template  
    latex_content = generator.generate_full_template(
        journal_name=args.journal,
        paper_title=args.title,
        authors=args.authors
    )
    
    filename = f"draft_{args.journal.replace(' ', '_')}.tex"
    generator.save_template(latex_content, filename)
    
    print("\n📝 Quick Start Guide:")
    print("  1. cd", output_dir) 
    print("  2. Fill in sections marked as TODO")  
    print("  3. Add your actual content to relevant sections") 
    print("  4. Run: pdflatex -interaction=nonstopmode draft.tex")
    print("  5. Check for compilation errors\nFor journal-specific formatting requirements, review the template code comments.")


if __name__ == "__main__":
    main()