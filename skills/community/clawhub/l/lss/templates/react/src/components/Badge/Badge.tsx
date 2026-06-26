import React from "react";
import "./Badge.css";

type BadgeVariant = "success" | "warning" | "error" | "info";

type BadgeProps = {
  variant?: BadgeVariant;
  children: React.ReactNode;
  className?: string;
};

export function Badge({ variant = "info", children, className = "" }: BadgeProps) {
  return <span className={["badge", `badge--${variant}`, className].filter(Boolean).join(" ")}>{children}</span>;
}
