import React from "react";
import "./Input.css";

type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  hint?: string;
  error?: string;
};

export function Input({ label, hint, error, id, className = "", ...props }: InputProps) {
  const inputId = id ?? React.useId();

  return (
    <div className="input-group">
      {label ? (
        <label className="input-label" htmlFor={inputId}>
          {label}
        </label>
      ) : null}
      <input id={inputId} className={["input-control", className].filter(Boolean).join(" ")} {...props} />
      {error ? <div className="input-error">{error}</div> : hint ? <div className="input-hint">{hint}</div> : null}
    </div>
  );
}
