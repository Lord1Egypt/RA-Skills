package com.teamtodo.util;

import javafx.geometry.Point2D;
import javafx.geometry.Rectangle2D;
import javafx.scene.control.TextInputControl;
import javafx.scene.input.InputMethodRequests;
import javafx.scene.text.Font;
import javafx.scene.text.Text;

/**
 * 修复 JavaFX 在 Windows 上 IME 候选框不跟随光标的问题。
 */
public class ImeHelper {

    private static final Text helper = new Text();

    public static void fixImeTracking(TextInputControl textInput) {
        textInput.setInputMethodRequests(new InputMethodRequests() {
            @Override
            public Point2D getTextLocation(int offset) {
                try {
                    String textBefore = textInput.getText();
                    if (textBefore == null) textBefore = "";
                    int caret = textInput.getCaretPosition();
                    if (caret > textBefore.length()) caret = textBefore.length();
                    String sub = textBefore.substring(0, caret);

                    Font font = textInput.getFont();
                    if (font != null) helper.setFont(font);
                    helper.setText(sub);
                    double textWidth = helper.getLayoutBounds().getWidth();

                    // padding
                    double paddingLeft = 5;
                    double paddingTop = 3;

                    Point2D local = new Point2D(paddingLeft + textWidth, paddingTop + textInput.getHeight());
                    Point2D screen = textInput.localToScreen(local);
                    return screen != null ? screen : new Point2D(0, 0);
                } catch (Exception e) {
                    return new Point2D(0, 0);
                }
            }

            @Override
            public int getLocationOffset(int x, int y) {
                return 0;
            }

            @Override
            public void cancelLatestCommittedText() {
            }

            @Override
            public String getSelectedText() {
                return textInput.getSelectedText();
            }
        });
    }
}
