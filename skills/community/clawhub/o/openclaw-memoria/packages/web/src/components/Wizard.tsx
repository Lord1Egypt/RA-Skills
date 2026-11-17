/**
 * Wizard — coquille réutilisable pour un parcours en étapes.
 * Affiche une barre de progression, le corps de l'étape courante et un pied
 * de page avec navigation. La logique métier reste dans l'écran appelant.
 */
import type { ReactNode } from "react";

export interface WizardStep {
  /** Identifiant stable de l'étape. */
  id: string;
  /** Titre court affiché en tête de l'étape. */
  title: string;
  /** Contenu de l'étape. */
  render: () => ReactNode;
}

interface WizardProps {
  steps: WizardStep[];
  /** Index de l'étape courante (0-based). */
  current: number;
  /** Demande d'aller à l'étape précédente. */
  onBack: () => void;
  /** Demande d'aller à l'étape suivante. */
  onNext: () => void;
  /** Action de fin (sur la dernière étape). */
  onFinish: () => void;
  /** Action « passer » l'onboarding (optionnelle). */
  onSkip?: () => void;
  /** Libellé du bouton « suivant » (peut varier selon l'étape). */
  nextLabel?: string;
  /** Désactive le bouton suivant/terminer (étape incomplète, chargement…). */
  nextDisabled?: boolean;
}

export function Wizard({
  steps,
  current,
  onBack,
  onNext,
  onFinish,
  onSkip,
  nextLabel,
  nextDisabled,
}: WizardProps) {
  const step = steps[current];
  const isFirst = current === 0;
  const isLast = current === steps.length - 1;
  if (!step) return null;

  return (
    <div className="wizard">
      <div className="wizard-steps" aria-hidden>
        {steps.map((s, i) => (
          <div key={s.id} className={`wizard-step-dot${i <= current ? " done" : ""}`} />
        ))}
      </div>

      <h1>{step.title}</h1>
      <div className="wizard-body">{step.render()}</div>

      <div className="wizard-footer">
        <div>
          {!isFirst && (
            <button type="button" className="btn-ghost btn" onClick={onBack}>
              Retour
            </button>
          )}
        </div>
        <div style={{ display: "flex", gap: 12 }}>
          {onSkip && !isLast && (
            <button type="button" className="btn btn-ghost" onClick={onSkip}>
              Passer
            </button>
          )}
          <button
            type="button"
            className="btn"
            disabled={nextDisabled}
            onClick={isLast ? onFinish : onNext}
          >
            {nextLabel ?? (isLast ? "Terminer" : "Continuer")}
          </button>
        </div>
      </div>
    </div>
  );
}
